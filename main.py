import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["bags"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url_template = 'https://momsbox.kz/catalog/womens/bags/?PAGEN_1={}'
page_number = 18
while True:

    url = url_template.format(page_number)
    response = requests.get(url, headers=headers)
    print('page number: ', page_number, url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all("div", {"class": "catalog-section-item-wrapper"})

    if len(items) == 0 or page_number == 25:
        print(page_number)
        break

    for item in items:
        name = item.find("a", {"class": "section-item-name"}).text.strip()
        price = item.find("div", {"class": "catalog-section-item-price-base"}).text.strip()
        price = price.replace(' ', '').replace('₸', '')
        price_int = int(price.replace('\xa0', ''))
        link = "https://momsbox.kz" + item.find("a", {"class": "section-item-name"})["href"]
        data = {
            "name": name,
            "price": price_int,
            "link": link
        }
        collection.insert_one(data)

    page_number += 1
client.close()
