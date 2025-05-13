import sys 
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import aglobal as gl # for modifying any global variables 
from aglobal import *

def valid_country(value:int): 
    if (value < 1): # base case
        return False
    match gl.country_ip[value]:
        # most of the ip addresses will be american, however not exclusively
        # filtered out countries where products are restricted
        case "United States" | "Germany" | "United Kingdom" | "South Africa" | "Brazil" | "Ireland" | "Australia" | "Mexico" | "Italy" | "France":
            return True
        case _:
            return False

# checks if ip is VALID or not
def valid_ip(ip:str):
    try: 
        ipaddress.ip_address(ip) # throws an exception if the ip isnt valid
        return True # if no exception, return true
    except ValueError: # catches a value error
        return False


class Proxy:
    """container for a proxy"""

    def __init__(self, ip, type_="datacenter") -> None:
        self.ip: str = ip
        self.type: Literal["datacenter", "residential"] = type_
        _, _, self.subnet, self.host = ip.split(":")[0].split('.')
        self.status: Literal["alive", "unchecked", "dead"] = "unchecked"
        self.last_used: int = None

    def __repr__(self) -> str:
        return self.ip

    def __str__(self) -> str:
        return self.ip


class Rotator:
    """weighted random proxy rotator"""

    def __init__(self, proxies: List[Proxy]):
        self.proxies = proxies
        self._last_subnet = None

    def weigh_proxy(self, proxy: Proxy):
        weight = 1_000
        if proxy.subnet == self._last_subnet:
            weight -= 500
        if proxy.status == "dead":
            weight -= 500
        if proxy.status == "unchecked":
            weight += 250
        if proxy.type == "residential":
            weight += 250
        if proxy.last_used: 
            _seconds_since_last_use = time() - proxy.last_used
            weight += _seconds_since_last_use
        return weight

    def get(self):
        proxy_weights = [self.weigh_proxy(p) for p in self.proxies]
        proxy = random.choices(
            self.proxies,
            weights=proxy_weights,
            k=1,
        )[0]
        proxy.last_used = time()
        self.last_subnet = proxy.subnet
        return proxy




if __name__ == "__main__":
    proxies = [
        # these will be used more often
        Proxy("xx.xx.422.1", "residential"),
        Proxy("xx.xx.812.2", "residential"),
        Proxy("xx.xx.221.3", "residential"),
        # these will be used less often
        Proxy("xx.xx.422.1"),
        Proxy("xx.xx.152.2"),
        Proxy("xx.xx.043.1"),
        Proxy("xx.xx.332.2"),
    ]
    
    proxies = []
    
    for i in range(0,234):
        curr = ""
        country = 0
        
        # runs while theres an ip duplicate OR curr is empty (initial)
        while(proxies.count(curr) >0 or curr == ""):
            country = 0
            while not (valid_country(country)):
                country = random.randint(1,223)
            
            curr =str(country) + "." 
            curr += str(random.randint(1,255)) + "." 
            curr +=str(random.randint(1,255)) + "." 
            curr +=str(random.randint(1,255))
        
        proxies.append(Proxy(curr, "residential") if (i<i/2 -2) else Proxy(curr))    
        
    rotator = Rotator(proxies)

    # let's mock some runs:
    _used = Counter()
    _failed = Counter()
    def mock_scrape():
        proxy = rotator.get()
        _used[proxy.ip] += 1
        if proxy.host == "1":  # simulate proxies with .1 being significantly worse
            _fail_rate = 60
        else:
            _fail_rate = 20
        if random.randint(0, 100) < _fail_rate:  # simulate some failure
            _failed[proxy.ip] += 1
            proxy.status = "dead"
            mock_scrape()
        else:
            proxy.status = "alive"
            #print(proxy.ip)
            return
    for i in range(0,10000):
        mock_scrape()

    for proxy, count in _used.most_common():
        print(f"{proxy} was used   {count:>5} times")
        print(f"                failed {_failed[proxy]:>5} times")
        
        
        
import httpx

with httpx.Client(
    # enable HTTP2 support
    http2=True,
    # set headers for all requests
    headers={"x-secret": "foo"},
    # set cookies
    cookies={"language": "en"}
    # set proxxies
    
) as session:
    session.get("https://httpbin.dev/get")