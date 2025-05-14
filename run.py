import requests
import multiprocessing
from multiprocessing.pool import Pool
import json
import time
import os
import re


url = 'https://scraper-api.decodo.com/v2/scrape'
username = os.getenv('USERNAME_DECODO')
password = os.getenv('PASSWORD_DECODO')


# "authorization": "Basic " + os.getenv('AUTH_DECODO')




def product_id(link:str)->str: # gets the unique amazon product id from the link 
    
    _, id = link.lower().split('/dp/', 2)
    #return 'https://www.amazon.com/'+ ('dp/' if '/dp/' in link else 'gp/offer-listing/') + id[:10].upper()  + '/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW'
    return id[:10].upper()
    
    
    
def phone_num(link:str)->str: # gets the phone number from the link 
    payload = {
      "url": link,
      "headless": "html"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers, auth=(username,password))
    
    index = response.text.find('seller-contact-phone')
    if(index>-1): # if seller phone number DOES exist
        return response.text[index+35:index+53].split('<')[0] # phone number found
    else: 
        return '' # NO PHONE NUMBER FOUND
    
    

# testing purposes
link='https://www.amazon.com/DP/B0015PBPJ4?th=1'
def run(link:str):
    
    listings = []
    listings_duped={} # pairs soon to be dicts (unduplicated)
    
    pool = Pool(processes=5)
    pool_res = []
    # flops between list of tuples and dicts
    
    i = 1
    while(True):
        payload = {
              "target": "amazon_pricing",
              "query": product_id(link=link),
              "page_from": str(i),
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
        
        orig_len = len(info['pricing'])
        if (orig_len <= 1):
            break

        if(i==1):
            original_listing = info['pricing'][0]
            info['pricing'].pop(0)
        #listings = list(dict([(elem['seller'], elem) for elem in info['pricing']]).values())
        #print(info['pricing'])
        #list(dict([(elem['author'], elem) for elem in a]).values())

        listings_duped = list(listings_duped.items()) # casts to list of tuples
        duped_len = len(listings_duped) # original duped length
        
        for listing in info['pricing']:
            if ( 
                listing['seller'] != original_listing['seller'] and
                listing['seller'] != 'Amazon Resale' and 
                listing['seller'] !='Amazon.com' and
                not any(i.isdigit() for i in listing['seller'])
                ):
                
                
                listings_duped.append((listing['seller'], listing))


        listings_duped = dict(listings_duped) # removes the duplicates
        
        
        if(duped_len == len(listings_duped)):  # if no change (repeats infinitely)
            break
        
        print(['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]])
        pool_res.append(pool.map_async(phone_num, ['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]]))
        
        
        #print(['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]])
        
        # for seller in list(listings_duped.values())[duped_len:]:
        #     listings_duped[seller]['phone number'] = phone_num('https://www.amazon.com' + listings_duped[seller]['seller_link'])
        #     #print(seller ,' :   ', listings_duped[seller]['seller_link'])
        print()
        
        # for listing in listings_duped.values():
        #     if 'phone number' not in listing:
        #         listing['phone number'] = phone_num('https://www.amazon.com/' + listing['seller_link'])
        
        
        #print(listings)
        
        #listings.append(list(dict(listings_duped).values()))
    

        if(orig_len<10):
            break
        # iterates through all listings that arent the first
        # first listing is the original seller's
        i+=1
    
    listings = list(dict(listings_duped).values()) # gets the values from the dicts
    
    pool.close()
    pool.join()
    
    if(len(listings) == 0):
        print(title, link, 'NO SELLERS FOUND', sep='\t')
    else:
        sellers = [listing['seller']  for listing in listings]
        #listings = list(dict(listings_new).values())
        # ACQUIRES ALL THE ELEMENTS
        # can start this process (phone # extraction) in the loop in the background
        print(title, link, sellers, sep='\t')
        #print(title, link, listings, sep='\t')
        
        i = 0
        success = 0
        for batch in pool_res:
            for number in batch.get():
                print(sellers[i], number, len(number))
                i+=1
        if(success==0):
            print('NO PHONE NUMBERS FOUND')
    
    
    

run(link)

pool = Pool()

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
#         r.get()
        
#         # shutdown the process pool
#         pool.close()
#         # wait for tasks to complete
#         pool.join()
#         # report all tasks done
#         print('All tasks are done', flush=True)
