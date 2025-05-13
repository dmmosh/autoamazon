import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os


  
import requests
  
url = "https://scraper-api.decodo.com/v2/scrape"
  
payload = {
      "target": "amazon_product",
      "query": "B09H74FXNW",
      "parse": True,
      "autoselect_variant": False
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic " + os.getenv('AUTH_DECODO')
}
  
response = requests.post(url, json=payload, headers=headers)
  
print(response.text)


def get_ip(i):
    response = requests.post(url, json=payload, headers=headers)
    r = json.loads(str(json.loads(response.text)['results'][0]['content']))['origin']
    print(str(i) + ' ip of sender: ' + r)


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
