import os
import time
import sys
from run import *
import run as r
import csv

links = []
with open(sys.argv[1], "r") as file:
    for link in file.read().splitlines():
        if link not in links:
            links.append(link)

file_path = sys.argv[1]
last_modified = os.path.getmtime(file_path)

i = 1

print("AUTO UPDATE DAEMON RUNNING")
with open(sys.argv[2], 'a') as file: # creates the file if it isnt there already
    pass

def link_run(link:str):
    product = run(link)
                    
    if(len(product) >0):
        with open(sys.argv[2], 'a') as file:
            writer = csv.writer(file,delimiter=';')
            rows = [product['link'], product['title'], product['asin']]
            rows.extend(list(sum(product['contacts'].items(), ())))
            #print(product['contacts'])
            #print(rows)
            writer.writerow(rows)
            print('product saved in','\"'+sys.argv[2]+'\"', sep='\t')


try:
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("File modified at:", time.ctime(current_modified))
            last_modified = current_modified
            current = open(sys.argv[1], "r").read().splitlines()
            #print(current)
            new = list(set(current) - set(links))

            if(len(new)>0):
                links.extend(new)
                print('newly added unique links:')
                print(new) # new is newly added, UNIQUE elements
                
                
                #pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
                #print(batch)
                #task = pool.submit(run, new)

                #batch = task.result()

                #print(batch)
                if 'END' in new:
                    print('DAEMON DONE. CLOSING')
                    os._exit()
                
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(link_run, new)
                
                
                # for link in new:
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

                print('BATCH ', i, 'DONE', sep='\t')
                i+=1

            else:
                print('no newly added unique links.')
        time.sleep(1)  # check every 1 second
except KeyboardInterrupt:
    print("Stopped watching.")
