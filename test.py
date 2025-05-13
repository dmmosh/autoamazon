
import random
import ipaddress
import httpx
import requests
from time import time
from time import sleep
from typing import List, Literal
from collections import Counter
import json
import signal

# tor_proxy_example.py
from tor_proxy import tor_proxy
from tor_proxy import onion
import requests
import atexit
import psutil



ports = [tor_proxy() for i in range(0,10)]


#atexit.register(onion.Onion.cleanup)
#signal.signal(signal.SIGINT, lambda: onion.Onion.cleanup(self))  # Ctrl+C
#signal.signal(signal.SIGTERM, lambda: onion.Onion.cleanup) # Termination signal

for port in ports:
    http_proxy  = f"socks5h://127.0.0.1:{port}"
    print(http_proxy)
    #https_proxy = f"socks5h://127.0.0.1:{port}"

    r = httpx.get("https://httpbin.org/ip", proxy=http_proxy)
    ip = json.loads(r.text)["origin"] # end node ip address - not the front node ip, pair them
    print(ip)
    
current_process = psutil.Process()
children = current_process.children(recursive=True)
for child in children:
    print('Child pid is {}'.format(child.pid))

