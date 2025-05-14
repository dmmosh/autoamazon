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


