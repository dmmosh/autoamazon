
import random
import ipaddress
import httpx
import requests
from time import time
from time import sleep
from typing import List, Literal
from collections import Counter
from fp.fp import FreeProxy # TESTINGG PURPOSES ONLY, use a good, paid proxy later


# tweak values
proxy_num = 5


# dont touch
country_ip = ["Australia","Germany","United States","United States","Italy","United States","United States","United States","United States","United States","United States","United States","China","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United Kingdom","United States","South Korea","United States","United States","United States","Germany","United States","United States","United States","United States","China","Germany","United States","Indonesia","United States","South Africa","China","Singapore","United States","Ghana","Germany","China","United States","China","United States","United States","United States","Germany","United States","United States","United States","United States","China","China","China","China","United Kingdom","Germany","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","France","United States","United States","Italy","France","United States","United States","Germany","France","Ireland","India","Thailand","France","Germany","Sweden","United States","Italy","Sweden","United States","United States","United States","Germany","United States","China","Mauritius","China","United States","Kenya","China","United States","United States","Germany","China","China","China","China","China","China","China","China","China","China","Indonesia","China","China","China","China","China","Japan","United States","United States","United States","United States","United States","Japan","United States","United States","United States","United States","United States","United States","United States","United States","Canada","United States","United States","Netherlands","United States","United States","United States","United States","Japan","United States","United States","United States","Ghana","United States","United States","United States","United States","United States","United States","United States","United States","France","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","United States","China","Spain","Brazil","United Kingdom","Brazil","China","Venezuela","China","China","United States","Germany","Argentina","Mexico","Slovenia","Brazil","Venezuela","Colombia","United States","Germany","United Kingdom","United States","Kenya","South Africa","United States","United States","Brazil","Mexico","China","Australia","United States","United States","United States","United States","United States","United States","China","China","United States","United Kingdom","United States","United States","United States","Germany","Japan","Japan","Japan","Japan","China","China"]
