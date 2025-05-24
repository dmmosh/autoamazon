import requests
import multiprocessing
from multiprocessing.pool import Pool
import signal
import sys
import json
import time
import os
import csv
import re


url = 'https://scraper-api.decodo.com/v2/scrape'
username = os.getenv('USERNAME_DECODO')
password = os.getenv('PASSWORD_DECODO')

total_valid_links = 0
total_good_links = 0



def initializer():
    """Ignore CTRL+C in the worker process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def product_id(link:str)->str: # gets the unique amazon product id from the link 
    
    _, id = link.replace('/gp/product/','/dp/').lower().split('/dp/', 2)
    #return 'https://www.amazon.com/'+ ('dp/' if '/dp/' in link else 'gp/offer-listing/') + id[:10].upper()  + '/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW'
    return id[:10].upper()
    

def check_access(file, mode):
   try:
      open(file, mode)
      return True
   except PermissionError:
      return False
   
def wait_access(file,mode):
    first_loop = True
    while(check_access(file=file,mode=mode) == False):
        if(first_loop):
            print(file + ' access permissions error. Try closing the file. Waiting...')
            first_loop= False
        time.sleep(1)

def exit_msg():
    print('DAEMON DONE. CLOSING', 
                            'TOTAL VALID LINKS:\t' + str(total_valid_links),
                            'TOTAL GOOD LINKS:\t' + str(total_good_links),
                                sep='\n')
    if(total_good_links>0):
        print('saved in','\"'+os.path.abspath(out_file)+'\"', sep='\t')
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)


def post_safe(payload,headers,message=''):
    if(len(message)>0):
        print(message)
    fails = 0
    while(True):
        response = requests.post(url=url, json=payload, headers=headers, auth=(username,password))

        if(response.status_code == 200):
            if(len(message)>0):
                print(message,'DONE', sep='\t')
            return response

        if(fails>=3): # if failed 3 times
            link = 'link N/A'
            if 'url' in payload:
                link = payload['url']
            elif 'query' in payload:
                link = 'https://www.amazon.com/dp/' + payload['query']

            if(len(message)>0):
                print(message,'FAILED', link, sep='\t')
            return None
            
        msg = json.loads(response.text)
        if 'message' in msg and msg['message'] == 'Your current plan\'s quota has been reached. Upgrade your plan to continue scraping.':
            print('FATAL SUPER ERROR: OUT OF DECODO REQUESTS')
            print('Buy more API requests on https://dashboard.decodo.com/')
            print('last accessed link:')
            if 'url' in payload:
                print(payload['url'])
            elif 'query' in payload:
                print('https://www.amazon.com/dp/' + payload['query'])
            else:
                print('link N/A, look at previous links')

            os._exit(1)


        # if failed 
        print(response.text)
        fails+=1
        print('REQUEST FAILED, TRYING AGAIN')



    
def phone_num(link:str)->str: # gets the phone number from the link 
    # payload = {
    #   "url": link,
    #   "headless": "html"
    # }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json"
    # }
    # response = requests.post(url, json=payload, headers=headers, auth=(username,password))
    response = post_safe(
        payload = {
            "url": link,
            "headless": "html"
        },
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
    )
    if response is None:
        return ''

    
    index = response.text.find('seller-contact-phone')
    if(index>-1): # if seller phone number DOES exist
        return response.text[index:index+53].split('<',2)[0].split('>',2)[1] # phone number found
    else: 
        return '' # NO PHONE NUMBER FOUND
    



# testing purposes
#link = 'https://www.amazon.com/dp/B08PPYQ9W5?th=1'
def run(link):

    pool = Pool(initializer=initializer)
    
    listings = []
    listings_duped={} # pairs soon to be dicts (unduplicated)
    i=1

    pool_res = []
    # flops between list of tuples and dicts
    out = {
        'contacts':{}
    } # output dict: if succeeds, contains the product name, link, and a nested dictionary with companies and their phone numbers
    # only return if successful, otherwise print

    i = 1
    while(True):

        response=post_safe(
            payload = {
              "target": "amazon_pricing",
              "query": product_id(link=link),
              "page_from": str(i),
              "parse": True # true for json, false for html
            },
    
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            },
            message='processing seller page '+ str(i) +'...'
        )

        if response is None:
            return out
        

        info = json.loads(response.text)['results'][0]['content']['results']

        if(i==1): #only assigns in the first page number
            out['title'] = info['title']
            out['asin'] = info['asin']

            if (len(info['pricing']) == 0):
                print('LISTING CURRENTLY UNAVAILABLE', sep='\t')
                return out
            original_listing = info['pricing'][0]
            info['pricing'].pop(0)
        i+=1 # iterates the page number 

        orig_len = len(info['pricing'])
        if (orig_len <= 1):
            break
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
        
        #print(['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]])
        print('requesting seller contacts...', end='\t')
        pool_res.append(pool.map_async(phone_num, ['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]]))
        print('DONE')

        
        #print(['https://www.amazon.com' + listing['seller_link'] for listing in list(listings_duped.values())[duped_len:]])
        
        # for seller in list(listings_duped.values())[duped_len:]:
        #     listings_duped[seller]['phone number'] = phone_num('https://www.amazon.com' + listings_duped[seller]['seller_link'])
        #     #print(seller ,' :   ', listings_duped[seller]['seller_link'])
        
        
        # for listing in listings_duped.values():
        #     if 'phone number' not in listing:
        #         listing['phone number'] = phone_num('https://www.amazon.com/' + listing['seller_link'])
        
        
        #print(listings)
        
        #listings.append(list(dict(listings_duped).values()))
    

        if(orig_len<10):
            break
        # iterates through all listings that arent the first
        # first listing is the original seller's
    
    print('waiting on remaining seller contacts...', end='\t')
    listings = list(dict(listings_duped).values()) # gets the values from the dicts
    
    pool.close()
    pool.join()
    print('DONE')
    
    print(out['title'])
    if(len(listings) == 0):
        print('NO VALID SELLERS FOUND', sep='\t')

    else:
        sellers = [listing['seller']  for listing in listings]
        #listings = list(dict(listings_new).values())
        # ACQUIRES ALL THE ELEMENTS
        # can start this process (phone # extraction) in the loop in the background
        #print(title, link, sellers, sep='\t')
        #print(title, link, listings, sep='\t')
        
        i = 0
        #success = 0

        for batch in pool_res:
            
            for number in batch.get():
                if(len(number)>0):
                    out['contacts'][sellers[i]] = number
                    #out.append((sellers[i], number))
                    #success+=1
                i+=1

        if(len(out['contacts'])==0): # if no phone numbers found
            print('NO PHONE #S FOUND')
    
    return out


if __name__ == "__main__":
    
    if(len(sys.argv) < 3):
        print('Needs 2 arguments. ' + str(len(sys.argv)-1) +' were given.')
        
        print('python', sys.argv[0], '<input links file (csv)> <output phone #s file (csv)>')
        os._exit(0)
    
    input_file = sys.argv[1]
    out_file = sys.argv[2]
    prev = []

    wait_access(input_file, "r") # waits until the file is ready 
    with open(input_file, "r") as file:
        prev = list((file.read().splitlines()))

    last_modified = os.path.getmtime(input_file)

    print("AUTO UPDATE SELLERS DAEMON RUNNING")

    try:
        while True:
            curr_modified = os.path.getmtime(input_file)

            if curr_modified != last_modified: # new batch 
                print("File modified at:", time.ctime(curr_modified))
                last_modified = curr_modified
                curr = []
                with open(sys.argv[1], "r") as file:
                    curr = list((file.read().splitlines()))
                #print(curr)
                    
                new = list(set(curr) - set(prev))
                prev = curr


                batch_good_links = 0

                for link in new: # new is the batch 

                    if link.lower() == 'end': #ends the program
                        raise KeyboardInterrupt

                    
                    if (link.count('amazon.com')>0): # valid link, api calls made, 
                        print()
                        print(link, '\t')

                        product = run(link)

                        
                        if(len(product['contacts']) >0): # if there is a contact
                            rows = ['https://www.amazon.com/dp/' + product['asin'], product['title'], product['asin']] # product info

                            wait_access(out_file,'a')
                            with open(out_file, 'a', newline='', encoding='utf-8') as file:
                                for seller, phone in product['contacts'].items():
                                    out = rows.copy()
                                    out.append(seller)
                                    out.append(phone)
                                    csv.writer(file,delimiter=',').writerow(out)

                            
                            batch_good_links+=1
                            
                            print('saved in','\"'+out_file+'\"', sep='\t')

                    else:
                        print(link, 'invalid link, skipping', sep='\t')
                print('BATCH DONE', 
                                'GOOD LINKS:\t'+str(batch_good_links),
                                sep='\n')
                print()
                if(batch_good_links>0):
                    print('saved in','\"'+os.path.abspath(out_file)+'\"', sep='\t')



                        

                
                total_good_links+=batch_good_links
                
            time.sleep(1)  # check every 1 second
    except (KeyboardInterrupt, Exception) as e:
        print()
        exit_msg()
    else:
        exit_msg()


        
        

    #print(run(link))

    #pool = Pool()

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
