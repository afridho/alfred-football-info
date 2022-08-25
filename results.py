import requests
from bs4 import BeautifulSoup
import json
requests.packages.urllib3.disable_warnings()
import sys
from importlib import reload
from dl_logo import parent_folder_logo
from news import light_dark
reload(sys)

baseUrl = 'https://www.espn.com/soccer/team/'
# baseUrl = 'https://www.espn.com/soccer/team/fixtures/_/id/148/ned.psv'
# baseUrl = 'https://www.espn.com/soccer/team/results/_/id/359/arsenal'

try:
    division = sys.argv[1] or '' # eng.1
    club_code = sys.argv[2] or '' # MAN
    club_name = sys.argv[3] or '' # manchester-united
    club_id = sys.argv[4] or '' # 360
    param = sys.argv[5] or '' # for param results or fixtures
except:
    raise Exception('No query found')


def web_url(): 
    # url = f"{baseUrl}"
    url = f"{baseUrl}{param}/_/id/{club_id}/{club_name}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    page = requests.get(url, headers=headers, verify=False)
    return page.content

def scrap():
    soup = BeautifulSoup(web_url(), "html.parser")
    data = []
    index = 0
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
                    "competition" : competition
                    }
            data.append(obj)
    # print(json.dumps(data, indent=4))  
    return data
def check_time(time):
    char_skip = ['AM', 'PM', 'FT', 'AET', 'TBD'] # AM PM FullTime, Added ExtraTime
    return [True for x in char_skip if x in time]

def get_win_status(team_id=None, team_home_id=None, team_away_id=None, score=None):
    home_score = score.rsplit('-', 1)[0].strip()
    away_score = score.rsplit('-', 1)[1].strip()
    status = 0
    location_status = ''
    home_text = '(H)'
    away_text = '(A)'
    
    if home_score == away_score:
        status = 1
    elif home_score > away_score:
        home_win = True
    elif home_score < away_score:
        home_win = False
    
    
    #no need to compare team_away_id
    team_home_status = True if team_id == team_home_id else False
    if status == 1:
        location_status = home_text if team_home_status else away_text
    else:   
        if team_home_status and home_win:
            location_status = home_text
            status = 3
        elif team_home_status and not home_win:
            location_status = home_text
            status = 0
        elif not team_home_status and home_win:
            location_status = away_text
            status = 0
        elif not team_home_status and not home_win:
            location_status = away_text
            status = 3
    # return print(f"{location_status} {status}")

    switcher={
        0 : 'Lose 🔴',
        1 : 'Draw ⚪️',
        3 : 'Win 🟢'
        }
    text_status = switcher.get(status, "nothing")
    return (f"{location_status} {text_status}")

"""
Get win status format (club_id, team_home_id, team_away_id, score)
"""  
# get_win_status(359, 269, 359, '3 - 5') # (A) 3
# get_win_status(359, 269, 359, '5 - 3') # (A) 0
# get_win_status(359, 359, 269, '5 - 3') # (H) 3
# get_win_status(359, 359, 269, '3 - 5') # (H) 0
# get_win_status(359, 359, 269, '3 - 3') # (H) 1
# get_win_status(359, 269, 359, '3 - 3') # (A) 1


def football(search=None):
    projects = scrap()
    # projects = data_object()
    result = []
    for project in projects:
        if search is not None and ((project['team_home'].lower().find(search.lower()) == -1) and (project['team_away'].lower().find(search.lower()) == -1)):
            continue
        result.append({
            'title': f"{'▸  ' if project['index'] == 1 else ''}{project['team_home']} {project['score']} {project['team_away']}{'  ◂' if project['index'] == 1 else ''} {'' if check_time(project['time']) else ' ⏳️' + project['time']}",
            'subtitle': f"🕰️ {project['date']} ▸  {project['time']+'  ||  ' if check_time(project['time']) else (project['time'] + '  ||  'if check_time(project['time']) else '')}{project['competition']}{('  ||  ' +get_win_status(club_id, project['team_home_id'], project['team_away_id'], project['score'])) if project['score'] != 'v' else ''}",
            # 'subtitle' : f"{project['score']}",
            'valid' : False,
            # 'icon': {
            #     'path': ((f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png")) if len(project['team']['abbreviation']) < 10 else f"src/empty-icon.png" # check icon if empty
            # },
            'mods':{
                'alt':{
                    'subtitle' : 'FT = Full Time   ||   AET = Added Extra Time   ||   H = Home   ||   A = Away'
                },
                # 'ctrl' : {
                #     'subtitle' : f"{project['team_home_id']}"
                # }
            }
            
        })
    if not search:
        result.append({
                'title': f"Back",
                'subtitle': f"Back to select club.",
                'arg': (f"back\n{division}"),
                'valid' : True,
                'icon': {
                    'path': (f"{parent_folder_logo}/{division}/{division}{light_dark()}.png")
                },
            }) 
    return result
    
def main():
    SEARCH = sys.argv[6] if len(sys.argv) >= 7 else None
    posts  = football(search=SEARCH)
    data = json.dumps({ "items": posts }, indent=4)
    print(data)
    
def data_object(): # data dummy
    fileJson = f"debug/results.json"
    f = open(fileJson)
    posts = json.load(f)
    return posts


if __name__ == '__main__':
    main()