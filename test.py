import requests
  
url = "https://scraper-api.decodo.com/v2/scrape"
  
payload = {
      "target": "amazon",
      "url": "https://www.amazon.com/s?i=smart-home&s=exact-aware-popularity-rank&page=392",
      "parse": True
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic VTAwMDAyNjg2ODk6UFdfMWU1ZGVlZjYxODk5MGY5NzJiYmJiMjM2NDIyNTI4M2Ey"
}
  
response = requests.post(url, json=payload, headers=headers)
  
print(response.text)