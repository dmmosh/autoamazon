import os
import time



lines = []
with open("List 1.csv", "r") as file:
    for link in file.read().splitlines():
        if(link)
    content = [ for link in file.readlines()]
    print(content)

i = 0
while(i < 5):
    i+=1

print(i)
file_path = 'List 1.csv'
last_modified = os.path.getmtime(file_path)




print("AUTO UPDATE DAEMON RUNNING")

try:
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("File modified at:", time.ctime(current_modified))
            last_modified = current_modified
        time.sleep(1)  # check every 1 second
except KeyboardInterrupt:
    print("Stopped watching.")