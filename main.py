#!/bin/env python3
import argparse

import yaml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from amazon_purchaser import AmazonPurchaser

parser = argparse.ArgumentParser(
    description='Simple Purchasing Bot. A simple bot to purchase things on the internet.',
    epilog='View the source code here: https://github.com/ksdsouza/simple-purchasing-bot'
)
parser.add_argument(
    '--username',
    type=str,
    required=True,
    help='Your username to purchase the product'
)

parser.add_argument(
    '--password',
    type=str,
    required=True,
    help='Your password to purchase the product'
)

args = parser.parse_args()

settings = yaml.safe_load(open("./settings.yaml"))['config']

product_polling_seconds = settings['productPollingSeconds']
product_link = settings['productLink']
headless = settings.get('headless', True)

options = Options()

if headless:
    options.add_argument('--headless')

while True:
    driver = webdriver.Firefox(options=options)
    purchaser = AmazonPurchaser(
        driver=driver,
        amazon_url=product_link,
        product_polling_seconds=product_polling_seconds,
        username=args.username,
        password=args.password
    )

    try:
        purchaser.run()
        break
    except Exception:
        driver.close()
