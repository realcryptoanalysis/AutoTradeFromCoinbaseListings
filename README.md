# AutoTradeFromCoinbaseListings
Python code to trade cryptocurrencies whenever a new coin/token is listed on CoinbasePro.

This code accompanies an article I wrote called [*Trade Cryptocurrencies Based on Coinbase Listings*](https://www.realcryptoanalysis.com/trade-cryptocurrencies-based-on-coinbase-listings/), that describes how you can automatically buy a coin/token as soon as its listed on CoinbasePro. I wrote this code for instructional purposes, but I have been using it to buy and sell small amounts of cryptocurrencies. If you choose to use this code, please do so with caution! Start by testing with small amounts of money!

## Background
I recently wrote an article analyzing the "Coinbase Effect" in 2021. The "Coinbase Effect" refers to the pump in a token's price after it's listed on Coinbase. I wanted to determine if the price pump continues to exist today and if we can take advantage of this knowledge.

*[How a Coinbase Listing Impacts a Token’s Short-Term Price – A 2021 Analysis](https://www.realcryptoanalysis.com/how-a-coinbase-listing-impacts-short-term-price-a-2021-analysis/)*

I hypothesized that a Coinbase listing would lead to price pumps based on previous articles written on the topic. After completing my analysis, I found that the average token price increased up to one week following its listing. However, the majority of tokens decrease in price! This was a complete shock to me. The reason for this is that a few tokens skyrocketed in price up to +500%, skewing the average gains. To be clear, I'm not suggesting that you use this information to make trading decisions. That's entirely up to you.

Naturally, I decided to write the code to automate buying a token as soon as it's listed.

## Getting CoinbasePro Keys
To access your CoinbasePro account and submit trades via Python, you first need to create the account and set up your API keys. The process is simple, and tutorials on these topics are abundant, so I won’t give step-by-step instructions here. To create a CoinbasePro account, go to [*https://www.coinbase.com/signup*](https://www.coinbase.com/signup) and follow the instructions. After creating the account, you need to generate API keys which can easily be completed by following the instructions [here](https://cryptopro.app/help/automatic-import/coinbase-pro-api-key/). After following the instructions in the 2 links above, you should have a CoinbasePro account, an API key, a secret API key, and a pass phrase that goes along with the two API keys.

Remember to never share your API keys or pass phrase with anyone.

### Saving your API keys
Once you have your CoinbasePro account, API keys, and API pass phrase, you need to save them in a JSON file. In the repository, you'll find a file named `coinbase_pro_api_keys.json` that needs to be completed. Open the file in a text editor and insert the appropriate keys and pass phrase. Save the JSON file.

## Installation
You will need to install Python3 as well as the following Python packages which can be installed with pip or Anaconda.

```
pip install pytz
pip install git+git://github.com/danpaquin/coinbasepro-python.git
```

## How to Run

Now that everything is set up, you can run the code using the following command:

```
python3 auto_trade_coinbase.py <command line args>
```
where `<command line args>` must be replaced with the following command line arguments.

### Arguments
Here are the command line arguments you will need:

```
usage: auto_trade_coinbase.py [-h] -d AMOUNT_TO_TRADE_USD -coinbase_api
                              COINBASE_API_KEYS_FILE
 
optional arguments:
  -h, --help            show this help message and exit
  -d AMOUNT_TO_TRADE_USD, --amount_to_trade_usd AMOUNT_TO_TRADE_USD
                        Amount of money in USD that you want to trade.
  -coinbase_api COINBASE_API_KEYS_FILE, --coinbase_api_keys_file COINBASE_API_KEYS_FILE
                        Path to file with CoinbasePro API keys.
```
Note - make sure the amount you want to trade is in USD.

The following example command will purchase $10 USD worth of any new listed token on CoinbasePro. The easiest way to run the code is to simply edit the following example.

```
python3 auto_trade_coinbase.py -d 10 -coinbase_api coinbase_pro_api_keys.json
```