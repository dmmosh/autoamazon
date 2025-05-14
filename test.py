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




def product_id(link:str)->str: # gets the unique amazon product id from the link 
    
    _, id = link.lower().split('/dp/', 2)
    #return 'https://www.amazon.com/'+ ('dp/' if '/dp/' in link else 'gp/offer-listing/') + id[:10].upper()  + '/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW'
    return id[:10].upper()
    


# testing purposes
link = 'https://www.amazon.com/dp/B08PPYQ9W5?th=1'




def run(link):
  
    payload = {
          "target": "amazon_pricing",
          "query": product_id(link=link),
          "page_from": "1",
          "parse": True # true for json, false for html
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers, auth=(username,password))

    if (response.status_code != 200):
        print('GET REQUEST FAILED, TRYING AGAIN')
        response = requests.post(url, json=payload, auth=(username,password))

    info = json.loads(response.text)['results'][0]['content']['results']
    title = info['title']
    if (len(info['pricing']) <= 1):
        print(title, link, 'NO OTHER SELLERS FOUND', sep='\t')
        return
    
    original_listing = info['pricing'][0]
    #listings = list(dict([(elem['seller'], elem) for elem in info['pricing']]).values())
    print(info['pricing'])
    
    listings = []
    for listing in info['pricing'][1:]:
        if ( 
            listing['seller'] != original_listing['seller'] and
            listing['seller'] != 'Amazon Resale' and 
            listing['seller'] !='Amazon.com' and
            not any(i.isdigit() for i in listing['seller'])
            ):
            listings.append((listing['seller'], listing))
            
    
    [listing['seller'] for listing in listings]
    listings = list(dict(listings).values())
    
    # iterates through all listings that arent the first
    # first listing is the original seller's
    
    print(title, link, [listing['seller'] for listing in listings])

run(link)


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
