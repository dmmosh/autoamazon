import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os
import amsin

from bs4 import BeautifulSoup


import requests

# "authorization": "Basic " + os.getenv('AUTH_DECODO')


def product_id(link:str)->str:
    
    _, id = link.lower().split('/dp/', 2)
    return id[:10].upper()
    

print(product_id('www.amazon.com/DP/B01LETURZI'))


os._exit(1)
    
  
url = "https://scraper-api.decodo.com/v2/scrape"
  
payload = {
      "target": "amazon",
      "url": "https://www.amazon.com/dp/B09H74FXNW",
      "parse": True
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic " + os.getenv('AUTH_DECODO')
}
  
response = requests.post(url, json=payload, headers=headers)
  
print(response.text)


# def get_ip(i):
#     response = requests.post(url, json=payload, headers=headers)
#     r = json.loads(str(json.loads(response.text)['results'][0]['content']))['origin']
#     print(str(i) + ' ip of sender: ' + r)


# n = 20

# print('httpbin test (multiprocessing pool)')

# with Pool() as pool:
        
#             # issue tasks into the process pool
#         r = pool.map_async(get_ip, range(n))

        
#         # shutdown the process pool
#         pool.close()
#         # wait for tasks to complete
#         pool.join()
#         # report all tasks done
#         print('All tasks are done', flush=True)
