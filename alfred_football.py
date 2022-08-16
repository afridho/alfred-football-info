#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2022 Ridho Zega
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
from __future__ import print_function, absolute_import
import json
import sys
import random
import string
import os
from datetime import datetime
import requests
from isCached import doCache
from importlib import reload
from dl_logo import parent_folder_logo
reload(sys)

def get_data_json():
    url = 'https://api-football-standings.azharimm.site/leagues/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    response = requests.request("GET", url, headers=headers, verify=False)
    posts = response.json()
    return posts


def time_now():
    now = datetime.now()

    # dd/mm/YY H:M:S
    timeNow = now.strftime("%d %B, %Y %H:%M:%S")
    return timeNow

def parse_season(seasonName=None):
    return seasonName.replace(' ', '_').lower();

def check_season_number(seasonName=None):
    parse = seasonName.split(' ')[1] or 25
    return int(parse)


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

    if (be.compare_time('leagues', 2)):
        data_out = get_data_json() # get from internet
    else:
        data_out = data_object() # get from cache file
    
    projects = data_out['data']
    
    
    # variable to short
    sT = 'stats'
    dV = 'displayValue'
    oV = 'value'
    
    result = []
    for project in projects:
        if search is not None and project['name'].lower().find(search.lower()) == -1:
            continue
        
        result.append({
            'title': f"{project['name']}",
            'arg': f"{project['id']}",
            'valid' : True,
            'icon': {
                'path': (f"{parent_folder_logo}{project['id']}/{project['id']}.png") if os.path.exists(f"{parent_folder_logo}{project['id']}/{project['id']}.png") else (f"{parent_folder_logo}/no-logo.png") # check icon if empty
            },
            # "action": {
            #     "text": project['team']['displayName'],
            # },
            # 'quicklookurl' : 'w'
            # 'text': {
            #     # "copy": project['url'],
            #     "largetype": f"{division}\n{project['team']['abbreviation']}\n{project['team']['displayName'].lower()}"
            # },
            'mods': {
                # 'alt': {
                #     'valid': True,
                #     # 'arg': project['id'],
                #     'subtitle': f"Rank : {get_rank_symbol(project[sT][8][oV])}"
                # },
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
        
    return result

"""Run Script Filter."""
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    division = os.getenv('fav_league')
    posts  = football(search=SEARCH, division=division)
    data = json.dumps({ "items": posts }, indent=4)
    print(data)
    

 
def data_object():
    fileJson = f"Cache/leagues.json"
    f = open(fileJson)
    posts = json.load(f)
    return posts



if __name__ == '__main__':
    # default load filter
    main()