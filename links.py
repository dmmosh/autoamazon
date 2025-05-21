from run import check_access
from run import wait_access
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

starting_page = 395    # starting page (inclusive)
ending_page = 380 # ending page (inclusive)


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





def iterate_category(args):
    
    
    link = 'https://www.amazon.com/s?i=' + str(args[0])+ '&s=exact-aware-popularity-rank&page=' + str(args[1])
    print(link)
    
    payload = {
        "target": "amazon",
        "url": link,
        "parse": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    print('processing', args[0], 'page', args[1], '...')
    response = requests.post(url, json=payload, headers=headers, auth=(username,password))
    print(args[0], 'case', args[1], end='\t')
    if(response.status_code!= 200):
        print('FAILED.\t LINKS NOT SAVED.')
        return [] # returns empty list if failed
    print('DONE')
    #print(response.text)
    info = json.loads(response.text)['results'][0]['content']['results']['results']
    if(len(info) == 0):
        return []
    info = [j for sublist in dict(info).values() for j in sublist]
    
    
    return [listing['asin'] for listing in info]


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
    