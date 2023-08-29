import aiohttp
import re
import os
import json
import requests
from bs4 import BeautifulSoup


def right_name(key: str,main_deck=None):
    url = f"https://ygocdb.com/?search={key}"
    headers = {
        'user-agent': 'Passerby_D',
        'referer': 'https://ygocdb.com/',
    }
    r = requests.get(url=url,headers=headers)

    soup = BeautifulSoup(r.text,'html.parser')
    infos = soup.findAll(class_ = 'desc')

    if main_deck:
        with open('./name2id.json','r',encoding='utf-8') as f:
            NameId = json.load(f)
        for info in infos:
            if '[怪兽' in str(info):
                name = re.findall('<span>(.*?)</span>',str(info))[0]
                if NameId[name] in main_deck:
                    return name 

    for info in infos:
        if '[怪兽' in str(info):
            name = re.findall('<span>(.*?)</span>',str(info))[0]
            return name
    

def name2id(name: str,main_deck=None):
    with open("name2id.json", "r", encoding="utf-8") as f:
        NameId = json.load(f)
    print(right_name(name,main_deck))
  
    return NameId[right_name(name,main_deck)]
