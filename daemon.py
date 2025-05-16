import os
import time
import sys
from run import *
import run as r
import csv

file_path = sys.argv[1]
prev = []
with open(file_path, "r") as file:
    prev = list(set(file.read().splitlines()))

last_modified = os.path.getmtime(file_path)

total_api_calls = 0
total_valid_links = 0
total_good_links = 0

print("AUTO UPDATE DAEMON RUNNING")


# def link_run(link:str):
#     product = run(link)
                    
#     if(len(product) >0):
#         with open(sys.argv[2], 'a') as file:
#             writer = csv.writer(file,delimiter=';')
#             rows = [product['link'], product['title'], product['asin']]
#             rows.extend(list(sum(product['contacts'].items(), ())))
#             #print(product['contacts'])
#             #print(rows)
#             writer.writerow(rows)
#             print('product saved in','\"'+sys.argv[2]+'\"', sep='\t')


try:
    while True:
        curr_modified = os.path.getmtime(file_path)

        if curr_modified != last_modified: # new batch 
            print("File modified at:", time.ctime(curr_modified))
            last_modified = curr_modified
            curr = []
            with open(sys.argv[1], "r") as file:
                curr = list(set(file.read().splitlines()))
            #print(curr)
                
            new = list(set(curr) - set(prev))
            prev = curr


            batch_api_calls = 0
            batch_valid_links=0
            batch_good_links = 0

            for link in new: # new is the batch 

                if link.lower() == 'end': #ends the program
                    raise KeyboardInterrupt

                
                if (link.count('amazon.com')>0): # valid link, api calls made, 
                    if(batch_valid_links==0): # if it's the first valid link
                        print('newly added link(s):')
                    print(link, '\t')
                    batch_valid_links+=1

                    product = run(link)
                    batch_api_calls+=product['api_calls']
                    if(len(product) >0):
                        rows = [product['link'], product['title'], product['asin']]
                        rows.extend(list(sum(product['contacts'].items(), ())))
                        with open(sys.argv[2], 'a') as file:
                            #print(product['contacts'])
                            #print(rows)
                            csv.writer(file,delimiter=';').writerow(rows)
                        batch_good_links+=1
                        
                        print('product saved in','\"'+sys.argv[2]+'\"', sep='\t')

                else:
                    print(link, 'invalid link, skipping', sep='\t')
            print('BATCH DONE', 
                          'API CALLS:\t'+ str(batch_api_calls), 
                          'VALID LINKS:\t'+str(batch_valid_links),
                            'GOOD LINKS:\t'+str(batch_good_links),
                              sep='\n')


                    

            
            total_api_calls+=batch_api_calls
            total_valid_links+=batch_valid_links
            total_good_links+=batch_good_links
            





        time.sleep(1)  # check every 1 second
except KeyboardInterrupt:
    print('DAEMON DONE. CLOSING', 
                          'API CALLS TOTAL:\t'+ str(total_api_calls), 
                          'VALID LINKS TOTAL:\t'+str(total_valid_links),
                            'GOOD LINKS TOTAL:\t'+str(total_good_links),
                              sep='\n')
