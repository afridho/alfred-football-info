#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2022 Ridho Zega
#
# MIT License. See http://opensource.org/licenses/MIT
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
from settings import data_settings
reload(sys)

baseUrl = os.environ['baseUrl']
data_year = os.environ['data_year']
# baseUrl = 'https://api-football-standings.azharimm.site/leagues'
# data_year = '2022'

def get_data_json(division=None):
    url = f"{baseUrl}/{division}/standings?season={data_year}&sort=asc"
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


def football(search=None, division=None):
    settings_file = data_settings()
    cache_time = settings_file['cache_time_hours'] or ''
    
    be = doCache()
    if (be.compare_time(division, cache_time)):
        data_out = get_data_json(division) # get from internet
    else:
        data_out = data_object(division) # get from cache file
    
    # projects = data_out['data']['standings'] if data_out['status'] else []
    # index = next((i for i, item in enumerate(projects) if item['team']['displayName'] == 'Everton'), -1)
    
    # projects.insert(0, projects.pop(index)) if index > 0 else ' ' # add favorite club to top

    #general variable
    club_fav_title = settings_file['favorite_club'] or ''
    club_fav_id = settings_file['favorite_club_id'] or ''
    league_fav_code = settings_file['favorite_club_league_code'] or ''
    favorite_text = os.environ['favorite_text'] or '============== 🄵🄰🅅🄾🅁🄸🅃🄴 🄲🄻🅄🄱 =============='
    # club_fav_title = 'Arsenal'
    # favorite_text = "=========="
    
    # variable to short
    sT = 'stats'
    dV = 'displayValue'
    oV = 'value'
    nl = '\n'
    
    result = []
    if data_out['status']:
        projects = data_out['data']['standings'] if data_out['status'] else []
        index = next((i for i, item in enumerate(projects) if item['team']['displayName'] == club_fav_title), -1)
        projects.insert(0, projects.pop(index)) if index > -1 else ' ' # add favorite club to top
        if(division == league_fav_code) and club_fav_id: # eng.1 and Arsenal (359)
            projects.append({"team" : {"displayName" : f"{favorite_text}", "abbreviation" : "LINE_FAVORITE", "id" : "-"}})
            projects.insert(1, projects.pop(len(projects) - 1)) if index > -1 else ' '
        
        for project in projects:
            if search is not None and (project['team']['displayName'].lower().find(search.lower()) == -1):
                continue
            result.append({
                'title': '{}{}'.format((project['team']['displayName']), '⭐️' if project['team']['displayName'] == club_fav_title else ''),
                'subtitle': '{} ▸  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}  ||  {}{}'.format((get_rank_symbol(project[sT][8][oV])),'MP=', project[sT][3][dV], 'Wins=', project[sT][0][dV], 
                                                            'Losses=', project[sT][1][dV], 'Draws=', project[sT][2][dV], 'GF=',project[sT][4][dV], 'GA=',project[sT][5][dV], 'Points=',project[sT][6][dV]) if 'stats' in project.keys() else '',
                'arg': (f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower().replace(' ','-')}\n{project['team']['id']}") if 'team' in project.keys() else '', # (eng.1) \n (MAN) \n Manchester United
                'valid' : True if 'stats' in project.keys() else False,
                'icon': {
                    'path': ((f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") if os.path.exists(f"{parent_folder_logo}{division}/{project['team']['abbreviation']}.png") else (f"{parent_folder_logo}/no-logo.png")) if len(project['team']['abbreviation']) < 10 else f"src/empty-icon.png" # check icon if empty
                },
                "variables": {"pickClub": project['team']['displayName']},
                "action": {
                    "text": project['team']['displayName'],
                },
                'text': {
                    "copy": (f"{project['team']['displayName']}") if 'team' in project.keys() else '',
                    "largetype": (f"{project['team']['displayName']}") if 'team' in project.keys() else '',
                },
                'mods': {
                    'alt': {
                        'valid': True,
                        'arg': (f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower().replace(' ','-')}\n{project['team']['id']}") if 'team' in project.keys() else '', # (eng.1) \n (MAN) \n Manchester United \n 360
                        'subtitle': f"🏛️ Get Fixtures Table of {project['team']['displayName']}",
                        'variables': {"pickClub": project['team']['displayName']}
                    },
                    'ctrl': {
                        'valid': True,
                        # add argument project finished to Dialog Conditional
                        'arg': f"{project['team']['displayName']+ nl + project['team']['id'] + nl + division + nl + 'Mark' if club_fav_id != project['team']['id'] else project['team']['displayName']+nl+''+nl+division+nl+'Remove'}",
                        'subtitle' : f"{'★ Mark this club as favorite' if club_fav_id != project['team']['id'] else 'Remove favorite'} ",
                    },
                    'cmd': { # get News
                        'valid': True,
                        'arg': (f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower().replace(' ','-')}") if 'team' in project.keys() else '', # (eng.1) \n (MAN) \n Manchester United
                        'subtitle': f"📰 Get News of {project['team']['displayName']}",
                    },
                }
            })
        if search == 'set' or search == '!' and len(search) > 0:
            result.append({
                    'title': f"Settings",
                    'subtitle': f"Football Info Configuration",
                    'arg': (f"settings"),
                    'valid' : True,
                    'icon': {
                        'path': (f"src/settings.png")
                    },
                })     
            
        if not search:
            result.append({
                    'title': f"Back",
                    'subtitle': f"Back to select leagues.",
                    'arg': 'back',
                    'valid' : True,
                    'icon': {
                        'path': f"src/back-icon.png",
                    },
            }) 
    else:
        result.append({
                'title': f"Back",
                'subtitle': f"Data not found.",
                'arg': 'back',
                'valid' : True,
                'icon': {
                    'path': f"src/back-icon.png",
                },
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

