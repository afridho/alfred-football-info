import json
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

baseUrl = 'https://www.espn.com/soccer/team/results/_/id/359/arsenal'

def web_url(): 
    url = f"{baseUrl}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    page = requests.get(url, headers=headers, verify=False)
    return page.content

def scrap():
    soup = BeautifulSoup(web_url(), "html.parser")
    data = []
    index = 0
    main_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(baseUrl)) # get https://www.espn.com
    for dl in soup.findAll("tbody", {"class" : "Table__TBODY"}):
        for dd in dl.findAll("tr", {"class" : "Table__TR"}):
            dt = dd.findAll('td')
            db = dd.findAll("a", href=True)
            if(len(dt) > 0):
                date = dt[0].text.strip()
                team_home = dt[1].text.strip()
                team_home_id = (db[1]['href']).rsplit('/', 2)[1]
                team_away = dt[3].text.strip()
                team_away_id = (db[3]['href']).rsplit('/', 2)[1]
                score = dt[2].text.strip()
                match_url = db[2]['href']
                time = dt[4].text.strip()
                competition = dt[5].text.strip()
                index += 1
                obj = {
                    "index" : index,
                    "date" : date,
                    "team_home" : team_home,
                    "team_home_id" : team_home_id,
                    "team_away" : team_away,
                    "team_away_id" : team_away_id,
                    "score" : score,
                    "time" : time,
                    "match_url" : f"{main_domain}{match_url}",
                    "competition" : competition
                    }
            data.append(obj)
    print(json.dumps(data, indent=4))  
    return data

scrap()