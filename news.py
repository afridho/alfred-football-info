# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from operator import index
import requests
from bs4 import BeautifulSoup
import sys
from importlib import reload
requests.packages.urllib3.disable_warnings()
reload(sys)
import json
import os
from dl_logo import parent_folder_logo
import shutil
import time

try:
    division = sys.argv[1] or '' # eng.1
    club_code = sys.argv[2] or '' # MAN
    news_tag = sys.argv[3] or '' # manchester-united
except:
    raise Exception('No query found')

# environment and variables
baseUrl = 'https://www.detik.com/tag/'
totalArticle = os.environ['total_article'] or 10

def icon_alfred():
    shutil.copy2((f"src/team-icons/{division}/{club_code}.png"), '3E4EF09C-A35E-43BB-80A7-4405449C5DE7.png')

def total_articles():
    return (int(totalArticle) // 10) + 1 

def web_url(pageNumber=None): 
    url = f"{baseUrl}{news_tag}/?sortby=time&page={pageNumber}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    page = requests.get(url, headers=headers, verify=False)
    return page.content

def get_data():
    data = []
    page_range = total_articles()
    index_number = 0
    for pageNum in range(1,page_range):
        soup = BeautifulSoup(web_url(pageNum), "html.parser")
        # print(web_url(pageNum))
        for dl in soup.findAll("article"):
            
            for dd in dl.findAll("a", href=True):
                url = dd['href']
            for dt in dl.findAll("h2", {"class" : "title"}):
                title = dt.text.strip()
            for do in dl.findAll("span", {"class": "date"}):
                soup.find('span', {'class': 'category'}).decompose() # ignore category class inside this date class
                date = do.text.strip()
            index_number += 1    
            obj = {
            "index" : index_number,
            "url": url,
            "title": title,
            "date" : date,
            }
            data.append(obj)
        
    # print(json.dumps(data, indent=4))
    return data


def news(search=None):
    
    news_data = get_data()
    result = []
    
    for news in news_data:
        if search is not None and news['title'].lower().find(search.lower()) == -1:
            continue
        
        result.append({
            'title': f"{news['title']}",
            'subtitle': f"#{news['index']} ▸ {news['date']}",
            'arg': news['url'],
            'valid' : True,
            'icon': {
                'path': (f"{parent_folder_logo}/{division}/{club_code}.png") # if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
            },
            "action": {
                "text": f"{news['title']} - {news['date']}\n\n{news['url']}",
            },
            'quicklookurl' : news['url'],
            'text': {
                "copy": news['url'],
                "largetype": news['title']
            },
        })
    result.append({
            'title': f"Back",
            'subtitle': f"Back to club.",
            'arg': f"back\n{division}\n{news['url']}",
            'valid' : True,
            # 'icon': {
            #     'path': (f"{parent_folder_logo}/{division}/{club_code}.png") # if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
            # },
        }) 
    return result

def main():
    # icon_alfred()
    # time.sleep(3)
    SEARCH = sys.argv[4] if len(sys.argv) >= 5 else None
    posts  = news(search=SEARCH)
    data = json.dumps({ "items": posts }, indent=4)
    print(data)
    
if __name__ == '__main__':
    # default load filter
    main() 