import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os


  
url = "https://scraper-api.decodo.com/v2/scrape"
  
payload = {
      "url": "https://httpbin.org/ip",
      "geo": "United States"
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic " + os.getenv('AUTH_DECODO')
}


def get_ip(i):
    response = requests.post(url, json=payload, headers=headers)
    r = json.loads(str(json.loads(response.text)['results'][0]['content']))['origin']
    print(str(i) + ' ip of sender: ' + r)


n = 20

print('httpbin test (multiprocessing pool)')

with Pool() as pool:
        
            # issue tasks into the process pool
        r = pool.map_async(get_ip, range(n))

        
        # shutdown the process pool
        pool.close()
        # wait for tasks to complete
        pool.join()
        # report all tasks done
        print('All tasks are done', flush=True)
