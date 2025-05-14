import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os
import amsin
import re

url = 'https://scraper-api.decodo.com/v2/scrape'
username = os.getenv('USERNAME_DECODO')
password = os.getenv('PASSWORD_DECODO')


# "authorization": "Basic " + os.getenv('AUTH_DECODO')



  
payload = {
      "url": "https://www.amazon.com/sp?ie=UTF8&seller=A2BH72QS89YRQE&isAmazonFulfilled=1&asin=B00Y8MP4G6&ref_=olp_merch_name_8",
      "headless": "html"
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
  
response = requests.post(url, json=payload, headers=headers, auth=(username,password))


index = response.text.find('seller-contact-phone')
if(index>-1): # if seller phone number DOES exist
    print(response.text[index+35:index+53].split('<')[0])
else: 
    print('NO PHONE NUMBER FOUND')