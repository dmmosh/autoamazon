import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os
import amsin




# "authorization": "Basic " + os.getenv('AUTH_DECODO')




def others_link(link:str)->str: # gets the unique amazon product id from the link 
    
    _, id = link.lower().split('/dp/', 2)
    return 'https://www.amazon.com/'+ ('dp/' if '/dp/' in link else 'gp/offer-listing/') + id[:10].upper()  + '/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW'
    


# testing purposes
link = 'https://www.amazon.com/dp/B09TX13F29'

url = "https://scraper-api.decodo.com/v2/scrape"

  
payload = {
      "target": "amazon_pricing",
      "query": "B09TX13F29",
      "page_from": "1",
      "parse": True
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic "+ os.getenv('AUTH_DECODO')
}
  
response = requests.post(url, json=payload, headers=headers)
  
print(response.text)


#print(others_link(link=link))

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
