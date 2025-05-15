
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    response = requests.get(url)
    return f"{url}: {response.status_code}"

urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.openai.com"
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(fetch, urls)

for result in results:
    print(result)