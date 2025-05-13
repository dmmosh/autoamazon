import sys 
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import aglobal as gl # for modifying any global variables 
from aglobal import *

def valid_country(value:int): 
    if (value < 1): # base case
        return False
    match gl.country_ip[(value-1)%len(gl.country_ip)]:
        # most of the ip addresses will be american, however not exclusively
        # filtered out countries where products are restricted
        case "United States" | "Germany" | "United Kingdom" | "South Africa" | "Brazil" | "Ireland" | "Australia" | "Mexico" | "Italy" | "France" | "Sweden":
            return True
        case _:
            return False



# doesnt check for duplicates in the list, simply creates valid ips
def ip_generator()-> str:
    ip = ""
    country = 0
    while not (valid_country(country)): # checks the country ip with the valid country list
        # filters out any restricted countries , that hide listings
        country = random.randint(1,223)
    
    ip += str(country) + "." 
    ip += str(random.randint(1,255)) + "." 
    ip += str(random.randint(1,255)) + "." 
    ip += str(random.randint(1,255))
    
    
    # final check (most ips are good, just in case)
    try:
        ipaddress.ip_address(ip) # checks if ip is valid, if not throws a value exception
        return ip
    except ValueError:
        return ip_generator()
        

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
    # proxies = [
    #     # these will be used more often
    #     Proxy("xx.xx.422.1", "residential"),
    #     Proxy("xx.xx.812.2", "residential"),
    #     Proxy("xx.xx.221.3", "residential"),
    #     # these will be used less often
    #     Proxy("xx.xx.422.1"),
    #     Proxy("xx.xx.152.2"),
    #     Proxy("xx.xx.043.1"),
    #     Proxy("xx.xx.332.2"),
    # ]
    
    proxies = []
    
    if(gl.proxy_num <= 4):
        print("MINIMUM PROXYY NUMBER IS 4")
        sys.exit()
    
    
    collector = proxyscrape.create_collector('my-collector', 'http')

    # Retrieve any http proxy
    proxy = collector.get_proxy()
    
    # Retrieve only 'us' proxies
    proxy = collector.get_proxy({'code': 'us'})
    
    # Retrieve only anonymous 'uk' or 'us' proxies
    proxy = collector.get_proxy({'code': ('us', 'uk'), 'anonymous': True})
    
    print(proxy)
    # for i in range(0,gl.proxy_num):
        
    #     ip = collector.get_proxy()
        
    #     # runs while theres an ip duplicate 
    #     # while(proxies.count(ip) >0):
    #     #     ip = ip_generator()
        
    #     print(ip)
    #     #proxies.append(Proxy(ip, "residential") if (i<i/2 -2) else Proxy(ip))    
        
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
        
        
        ip = "http://178.171.106.116:5433"
        print(ip)
        r = httpx.get("https://httpbin.io/ip", proxy=ip)
        print(r.text)
        
        fail = random.randint(0, 100) < _fail_rate
        
        if fail:  # simulate some failure
            _failed[proxy.ip] += 1
            proxy.status = "dead"
            mock_scrape() # tries again with new ip
        else: # SUCCESS
            proxy.status = "alive"
            #print(proxy.ip)
            return
    for i in range(0,5):
        mock_scrape()
        sleep(0.001)

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