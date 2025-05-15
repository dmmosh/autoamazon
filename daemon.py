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

print("AUTO UPDATE DAEMON RUNNING")

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
                
                
                pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
                #print(batch)
                task = pool.submit(run, new)

                batch = task.result()

                print(batch)
                
                #batch = r.run_all(new)

                with open(sys.argv[2], 'a') as file:
                    writer = csv.writer(file)

                    for product in batch:
                          


                        
                        rows = [product['link'], product['title'], product['asin']]
                        rows.extend(list(sum(product['contacts'].items(), ())))
                        #print(product['contacts'])
                        #print(rows)
                        writer.writerow(rows)
                        print('product saved in','\"'+sys.argv[2]+'\"', sep='\t')
                        

            else:
                print('no newly added unique links.')
        time.sleep(1)  # check every 1 second
except KeyboardInterrupt:
    print("Stopped watching.")
