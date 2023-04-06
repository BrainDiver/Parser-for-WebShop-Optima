import requests
import json
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class Product_item:
    url:str
    title: str
    price: str
    description:str

    def to_dict(self):
        return {"title": self.title, "description": self.description, "price": self.price, "url": self.url }
def product_list(query, start):
    print("Working")
    url= f"https://optima-computers.ru"
    headers={
             'User-Agent': 'Mozilla/5.70 (Windows NT 10.0; Win64; x64)'
            }
    params={"st": query}
    response= requests.get(url+"/search?", headers=headers, params=params).text
    print("Collecting item")
    soup= BeautifulSoup(response, "html.parser")
    search_result= soup.find("div")
    print("Almost done")
    item_results= search_result.find_all("div", {"class":"sale-img_wrap"})
    item_description_results= search_result.find_all("div", {"class":"description-tooltip"})
    item_price_results=search_result.find_all("div", {"class": "price-text"})
    products=[]
    for item in item_results:
        item_url=url + item.select_one("a").get("href")
        item_title= item.select_one("img").get("alt")
        item_description=item_description_results[item_results.index(item)].text.strip()
        item_price=item_price_results[item_results.index(item)].select_one("strong").text.strip()
        product_add=Product_item(title=item_title, description=item_description, price=item_price, url=item_url)
        products.append(product_add.to_dict())
        
    #i added all get information to list with dictionaries and now i can serialize it with json.dump
    #like this exit_results= json.dumps({"products": products})
    #but in my program i just print result
    
    for i in products:
        print(i.get("title"), i.get("description"), i.get("price"), i.get("url")," ", sep="\n")

    stop=time.time()-start
    print(f"Done {stop} sec")
def main():
    start=time.time()
    query= input('Query for search ')
    product_list(query,start)
main()
