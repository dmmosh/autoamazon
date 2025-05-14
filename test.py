import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os
import amsin


url = 'https://scraper-api.decodo.com/v2/scrape'
username = os.getenv('USERNAME_DECODO')
password = os.getenv('PASSWORD_DECODO')


# "authorization": "Basic " + os.getenv('AUTH_DECODO')



  
payload = {
      "url": "https://www.amazon.com/sp?ie=UTF8&seller=A1IB24DCGWL26X&isAmazonFulfilled=0&asin=B08X1SX524&ref_=olp_merch_name_9",
      "headless": "html"
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
  
response = requests.post(url, json=payload, headers=headers, auth=(username,password))
  
print(response.text)