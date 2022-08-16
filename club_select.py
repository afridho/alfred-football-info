#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2022 Ridho Zega
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
from __future__ import division, print_function, absolute_import
import json
import sys
import os
from datetime import datetime
import requests
from isCached import doCache
from importlib import reload
from dl_logo import parent_folder_logo
reload(sys)

def get_data_json(division=None):
    url = 'https://api-football-standings.azharimm.site/leagues/'+division+'/standings?season=2022&sort=asc'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    response = requests.request("GET", url, headers=headers, verify=False)
    posts = response.json()
    return posts

def get_rank_symbol(rank=None):
    switcher={
        1 : '🥇',
        2 : '🥈',
        3 : '🥉'
    }
    return switcher.get(rank,'#{}'.format(rank))
 
def get_status_lastMatched(point=None):
    num = float(point)
    if num > 0:
        return '✅'
    elif num == 0:
        return '✴️'
    else:
        return '🔴'


def football(search=None, division=None):
    be = doCache()
    if (be.compare_time(division, 8)):
        data_out = get_data_json(division) # get from internet
    else:
        data_out = data_object(division) # get from cache file
    
    
    # projects = data_out['data']['standings'] if data_out['status'] else []
    # index = next((i for i, item in enumerate(projects) if item['team']['displayName'] == 'Everton'), -1)
    
    # projects.insert(0, projects.pop(index)) if index > 0 else ' ' # add favorite club to top

    #general variable
    club_fav_title = os.environ['club_fav_title']
    
    # variable to short
    sT = 'stats'
    dV = 'displayValue'
    oV = 'value'
    
    result = []
    if data_out['status']:
        projects = data_out['data']['standings'] if data_out['status'] else []
        index = next((i for i, item in enumerate(projects) if item['team']['displayName'] == club_fav_title), -1)
        projects.insert(0, projects.pop(index)) if index > 0 else ' ' # add favorite club to top
        
        for project in projects:
            if search is not None and project['team']['displayName'].lower().find(search.lower()) == -1:
                continue
            
            result.append({
                'title': '{}{}'.format((project['team']['displayName']), '⭐️' if project['team']['displayName'] == club_fav_title else ''),
                'subtitle': '{} ▸  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}'.format((get_rank_symbol(project[sT][8][oV])),'MP=', project[sT][3][dV], 'Wins=', project[sT][0][dV], 
                                                            'Losses=', project[sT][1][dV], 'Draws=', project[sT][2][dV], 'GF=',project[sT][4][dV], 'GA=',project[sT][5][dV], 'Pts=',project[sT][6][dV], get_status_lastMatched(project[sT][9][oV])),
                'arg': f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower().replace(' ','-')}", # (eng.1) \n (MAN) \n Manchester United
                'valid' : True,
                'icon': {
                    'path': (f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
                },
                "action": {
                    "text": project['team']['displayName'],
                },
                # 'quicklookurl' : 'w'
                # 'text': {
                #     # "copy": project['url'],
                #     "largetype": f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower()}"
                # },
                'mods': {
                    'alt': {
                        'valid': True,
                        # 'arg': project['id'],
                        'subtitle': f"Rank : {get_rank_symbol(project[sT][8][oV])}"
                    },
                    # 'ctrl': {
                    #     'valid': True,
                    #     # add argument project finished to Dialog Conditional
                    #     'arg': '{}:{}'.format(project['id'],project['finished']),
                    #     'subtitle' : '{}'.format('🍿Mark Unwatched' if project['finished'] == True else '☑️Mark Watched'),
                    # },
                    # 'cmd': {
                    #     'valid': True,
                    #     'arg': 'Season ',
                    #     'subtitle': '➕Add season',
                    # },
                }
            })
        result.append({
                'title': f"Back",
                'subtitle': f"Back to select leagues.",
                'arg': 'back',
                'valid' : True,
                # 'icon': {
                #     'path': (f"{parent_folder_logo}/{division}/{club_code}.png") # if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
                # },
        }) 
    else:
        result.append({
                'title': f"Back",
                'subtitle': f"Data not found.",
                'arg': 'back',
                'valid' : True,
                # 'icon': {
                #     'path': (f"{parent_folder_logo}/{division}/{club_code}.png") # if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
                # },
        })     
    return result

"""Run Script Filter."""
def main():
    SEARCH = sys.argv[2] if len(sys.argv) >= 3 else None
    fav_league = os.getenv('fav_league')
    division = sys.argv[1] or fav_league
    # division = 'eng.1'
    posts  = football(search=SEARCH, division=division)
    data = json.dumps({ "items": posts }, indent=4)
    print(data)

def data_object(division=None):
    fileJson = f"Cache/{division}.json"
    f = open(fileJson)
    posts = json.load(f)
    return posts

if __name__ == '__main__':
    # default load filter
    main()

    
