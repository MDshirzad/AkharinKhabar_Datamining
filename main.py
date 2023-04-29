import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url="https://akharinkhabar.ir/"
politics="politics"
economy="money"
features=[politics,economy]
# features=[politics]

scraps=[]

def first_data():
    for item in features:
        data = requests.get(base_url+item).content
        soup=BeautifulSoup(data,features="html.parser")
        for tag in soup.find_all("li"):
            try:
                if tag:
                    if tag.get('class'):
                        if tag.get('class')[0] == 'live-feed-news-item':
                            if tag.a.h5.string:

                                news = {"group": item,
                                        "title": tag.a.h5.string,
                                        "link": "https://akharinkhabar.ir/" + tag.a.get('href'),
                                        "text":""}
                                scraps.append(news)

            except:
                pass
    return scraps

def detail_scrap():
    text=[]
    first =first_data()
    for i in first:
        response = requests.get(i["link"]).content
        soup=BeautifulSoup(response,"html.parser")
        p=soup.find_all("p",attrs={"id":"content-id"})[0].text
        i["text"]=p
    print(first)
    return first

def seperator():
    t = detail_scrap()
    features=[[],[]]
    for i in t:
        if i["group"]=="politics":
            features[0].append(i)
        elif i["group"]=="money":
            features[1].append(i)
    create_xlsx(features)


def create_xlsx(lis):
    counter=0
    for i in lis:
        counter+=1
        df= pd.DataFrame(i)
        df.to_excel(f"{counter}.xlsx")

seperator()