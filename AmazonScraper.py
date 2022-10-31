import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
from time import sleep

# Constants
URL = "URL"
PRICE = "price"
RATE_COUNT = "rate_count"
RATE = "rate"
PRODUCTS = "Products"
PARSER_LIB = "html.parser"
# Variable
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "es-US, en:q=0.5"
}
search_prod = "pencil"
search_query = search_prod.replace(" ", "+")
base_url = "https://www.amazon.com/s?k={0}".format(search_query)

items = []
df = pd.DataFrame(items, columns=[PRODUCTS, RATE, RATE_COUNT, PRICE, URL])

for i in range(1, 11):
    print(f"Url to scrapp: {base_url}")
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, PARSER_LIB)

    results = soup.find_all("div", {"class": "s-result-item",
                                    "data-component-type": "s-search-result"})

    for product in results:
        prod_name = product.h2.text

        try:
            rate = product.find("i", {"class": "a-icon"}).text
            rate_count = product.find("span", {"class": "a-size-base"}).text
        except AttributeError:
            print("AttributeError")
            continue

        try:
            prices_whole = product.find("span", {"class": "a-price-whole"}).text
            prices_fraction = product.find("span", {"class": "a-price-fraction"}).text
            price = float(prices_whole + prices_fraction)
            prod_url = "https://www.amazon.com" + product.h2.a["href"]
        except AttributeError:
            print("AttributeError")
            continue
        tmp_df = pd.Series({PRODUCTS: prod_name, RATE: rate, RATE_COUNT: rate_count, PRICE: price, URL: prod_url})
        df = pd.concat([df, tmp_df.to_frame().T],
                       ignore_index=True)
    sleep(2)
    print(f"pag {i}")

print(df.head())
