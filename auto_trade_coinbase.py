import argparse
import cbpro
from datetime import datetime
import json
import logging
import os
import pytz
import time


def create_logger(saved_dir):
    """Set up the logger."""
    files = os.listdir(saved_dir)
    ids = []
    for filename in files:
        if 'logger' in filename:
            id = int(between(filename, 'logger_', '.txt'))
            ids.append(id)

    if len(ids) > 0:
        new_id = max(ids) + 1
        logger_file_path = os.path.join(
            saved_dir, 'logger_{}.txt'.format(new_id))
    else:
        logger_file_path = os.path.join(saved_dir, 'logger_0.txt')

    logging.basicConfig(filename=logger_file_path,
                        filemode='a', level=logging.INFO)
    logger = logging.getLogger()

    return logger


def output_msgs(msg):
    """Print and log messages."""
    print(msg)
    logger.info(msg)


def between(input_str, start, end):
    """Utility method to get string between two substrings."""
    return input_str[input_str.find(start) + len(start):input_str.rfind(end)]


def set_up_coinbase_pro_api(path_to_keys_file):
    """Set up CoinbasePro Private API."""
    with open(path_to_keys_file) as f:
        coinbase_keys = json.load(f)

    key = coinbase_keys['coinbase_pro_api_key']
    secret_key = coinbase_keys['coinbase_pro_api_secret_key']
    passphrase = coinbase_keys['coinbase_api_pro_passphrase']

    client = cbpro.AuthenticatedClient(key, secret_key, passphrase)

    return client


def get_crypto_asset_set():
    """Get cryptocurrencies listed on CoinbasePro."""
    public_client = cbpro.PublicClient()
    response = public_client.get_products()
    initial_currs = {}

    for i in response:
        if (i['id'].endswith('-USD') and
            not i['cancel_only'] and
            not i['post_only'] and
            not i['trading_disabled'] and
            not i['auction_mode']):
            base_increment = str(i['base_increment'])[::-1].find('.')
            if base_increment == -1:
                base_increment = 0
            quote_increment = str(i['quote_increment'])[::-1].find('.')
            if quote_increment == -1:
                quote_increment = 0
            initial_currs[i['id']] = {'base_increment': base_increment,
                                      'quote_increment': quote_increment}

    return initial_currs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--amount_to_trade_usd',
                        type=float,
                        required=True,
                        default=10,
                        help="Amount of money in USD that you want to trade.")
    parser.add_argument('-coinbase_api',
                        '--coinbase_api_keys_file',
                        type=str,
                        required=True,
                        help="Path to file with CoinbasePro API keys.")

    args = parser.parse_args()

    # set up inputs
    amount_to_trade_usd = args.amount_to_trade_usd
    coinbase_api_keys_file = args.coinbase_api_keys_file

    # set up logger
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    saved_dir = os.path.join(curr_dir, 'saved_data')
    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir)
    logger = create_logger(saved_dir)

    msg = 'Info: Amount to trade - {}.\n'.format(amount_to_trade_usd)
    output_msgs(msg)

    # read CoinbasePro api keys
    client = set_up_coinbase_pro_api(coinbase_api_keys_file)
    msg = 'Set up Coinbase Pro API\n'
    output_msgs(msg)

    fee = float(client.get_fees()['maker_fee_rate'])

    master_currs_list = get_crypto_asset_set()

    msg = 'Continuously sampling CoinbasePro cryptocurrency list to find new tokens ...'
    output_msgs(msg)

    while True:
        try:
            currs = get_crypto_asset_set()
        except Exception as e:
            msg = 'ERROR: Could not gather current Coinbase cryptocurrency list - {}.'.format(e)
            output_msgs(msg)
            continue

        new_currs = currs.keys() - master_currs_list.keys()
        if new_currs:
            master_currs_list = currs
            msg = 'Found new listed cryptocurrencies: {}, at time: {}\n'.format(
                ', '.join(new_currs), datetime.now(pytz.timezone('UTC')))
            output_msgs(msg)

            for i in new_currs:
                buy_attempts = 0
                base_increment = currs[i]['base_increment']
                quote_increment = currs[i]['quote_increment']
                price_dict = client.get_product_ticker(product_id=i)
                if 'price' in price_dict:
                    price = float(price_dict['price'])
                else:
                    continue
                price_to_trade = round(price + price * 0.01, quote_increment)
                size = round(amount_to_trade_usd / price_to_trade, base_increment)
                account = client.get_accounts()
                for j in account:
                    if j['currency'] == 'USD':
                        balance = float(j['balance'])
                total_price_usd = price_to_trade * size

                if balance < total_price_usd + total_price_usd * fee:
                    msg = "Not enough USD to purchase {} {} at {} USD".format(size, i, price_to_trade)
                    output_msgs(msg)
                    break
                while buy_attempts <= 5:
                    try:
                        order = client.buy(product_id=i,
                                           price=price_to_trade,
                                           size=size,
                                           order_type='limit')
                        break
                    except:
                        buy_attempts += 1
                if buy_attempts > 5:
                    msg = "ERROR: could not buy {}".format(i)
                else:
                    msg = "Submitted buy order for {}. ".format(i)
                    msg += "Order size: {}. ".format(size)
                    msg += "Price: {}. ".format(price_to_trade)
                    msg += "Amound USD spent: {}\n".format(price_to_trade * size)
                output_msgs(msg)

        time.sleep(1)
