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
link = 'https://www.amazon.com/Turtle-Wax-53737-Patent-Pending-Anniversary/dp/B08X1SX524/?_encoding=UTF8&pd_rd_w=y5OoT&content-id=amzn1.sym.a602a706-e4fe-481e-98c3-9b75060fd322%3Aamzn1.symc.abfa8731-fff2-4177-9d31-bf48857c2263&pf_rd_p=a602a706-e4fe-481e-98c3-9b75060fd322&pf_rd_r=7CMD4G817TACD7BNWNAG&pd_rd_wg=9LGkO&pd_rd_r=41723a4e-59b1-490c-8a66-e214e1182c0a&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d'


def run(link):
    
    listings = []
    listings_duped={} # pairs soon to be dicts (unduplicated)
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
        if(orig_len < 10 or duped_len == len(listings_duped)):  # if no further elements OR no change (repeats infinitely)
            break
        
        #print(listings)
        
        #listings.append(list(dict(listings_duped).values()))
        

        # iterates through all listings that arent the first
        # first listing is the original seller's
        i+=1

    listings = list(dict(listings_duped).values())

    #listings = list(dict(listings_new).values())
    # ACQUIRES ALL THE ELEMENTS
    # can start this process (phone # extraction) in the loop in the background
    print(title, link, listings)
    
    
    
    

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
#         r.get()
        
#         # shutdown the process pool
#         pool.close()
#         # wait for tasks to complete
#         pool.join()
#         # report all tasks done
#         print('All tasks are done', flush=True)
