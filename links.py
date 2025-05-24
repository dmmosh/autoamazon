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

starting_page = 400 # default starting page (inclusive)
ending_page = 1 #default ending page  (inclusive)



import random 

'''
REFERENCE

https://www.amazon.com/s?i=electronics&s=exact-aware-popularity-rank&page=400




'''



url = 'https://scraper-api.decodo.com/v2/scrape'
username = os.getenv('USERNAME_DECODO')
password = os.getenv('PASSWORD_DECODO')

starting_page = 400    # starting page (inclusive)
ending_page = 20 # ending page (inclusive)


total_api_calls = 0
total_links=0
out_file = ""



categories = ['electronics',
              'beauty', 
              'luxury-beauty', 
              'tools', 
              'smart-home',  # ai nanotech super technology
              'pets', #anything for pets 
              'office-products', 
              'fashion-luggage',# luggage, bags 
              'industrial', # power tools
              'garden', # home and garden stuff. house stuff. 
              'hpc', # health, household, and baby care
              'lawngarden', # lawn and garden stuff 
              'computers'
]



def initializer():
    """Ignore CTRL+C in the worker process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


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

def price(cost):
    if isinstance(cost,float) or isinstance(cost,int):
        return cost
    return 0

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




def iterate_category(args):
    
    
    link = 'https://www.amazon.com/s?i=' + str(args[0])+ '&s=exact-aware-popularity-rank&page=' + str(args[1])
    print(link)
    
    out = []

    response = post_safe(
        payload = {
        "target": "amazon",
        "url": link,
        "parse": True
        },
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        },
        message= 'processing '+ str(args[0])+ ' page '+ str(args[1])+ ' ...'
    )
    if response is None:
        return out

    info = json.loads(response.text)['results'][0]['content']['results']['results']
    if(len(info) == 0):
        return []
    listings = [j for sublist in dict(info).values() for j in sublist]
    
    for listing in listings:
        if 'price' in listing and price(listing['price']) >=1:
            out.append(listing['asin'])

    
    return out


def exit_msg():
    print('DAEMON DONE. CLOSING', 
                            'API CALLS TOTAL:\t'+ str(total_api_calls), 
                            'LINKS GATHERED:\t' + str(total_links),
                                sep='\n')
    if(total_api_calls>0):
        print('MEAN LINKS PER PAGE:\t' + str(int(total_links/total_api_calls)))
    if(total_links>0):
        print('saved in','\"'+os.path.abspath(out_file)+'\"', sep='\t')
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)
    
    



if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('Needs 1 argument. 0 were given.')
        print('python', sys.argv[0], '<output links file (csv)>')
        os._exit(1)

    out_file = sys.argv[1]
    
    categories.extend(sys.argv[2:])
    
    
    
    #categories = ['beauty','electronics'] # testing purposes
    
    print("AUTO UPDATE LINK DAEMON RUNNING")
    
    
    
    try:
        pairs = [(category, i) for i in range(starting_page,ending_page-1,-1) for category in categories]
        with Pool(initializer=initializer) as pool:
            for result in pool.imap_unordered(iterate_category, pairs):
                #print(result)
                total_api_calls+=1 # api calls DONE (can be interruped)
                total_links += len(result) 
                
                if(len(result)>0):
                    wait_access(out_file,'a')
                    with open(out_file, 'a', newline='', encoding='utf-8') as file:
                            for asin in result:
                                csv.writer(file,delimiter=',').writerow(['https://www.amazon.com/dp/' + asin])

                # returns empty list if failed
       
    except (KeyboardInterrupt, Exception) as e:
        print()
        exit_msg()
    else:
        exit_msg()
    
    
    #print(categories)
    