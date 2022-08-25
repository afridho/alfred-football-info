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
from importlib import reload
reload(sys)

def get_data_options():
    fileJson = f"src/settings.json"
    f = open(fileJson)
    posts = json.load(f)
    
    cache_time_display = posts['cache_time_hours']
    
    data = [
        {
            "id" : 1,
            "option_name" : "Change Cache Time",
            "desc" : "Set Cache time to refresh again (in hour)",
            "info" : cache_time_display
        },
        {
            "id" : 2,
            "option_name" : "Remove Favorite Club",
            "desc" : "You can use ⌃ctrl button to mark/remove club",
            "info" : ''
        },
        {
            "id" : 3,
            "option_name" : "Reload Resources Logo",
            "desc" : "Download/Refresh All logo (use terminal and python3 to execute dl_logo.py)",
            "info" : ''
        }
            ]
    return data

def settings(search=None):
    data_options = get_data_options()
    
    result = []
    for data in data_options:
        if search is not None and (data['option_name'].lower().find(search.lower()) == -1):
            continue
        result.append({
            'title': f"{data['option_name']}",
            'subtitle': f"{data['desc']}",
            'arg' : f"{data['id']}",
            'valid' : True,
            'variables': {"cacheTime": data['info']},
            'icon': {
                'path': f"src/settings.png"
            },
            })
        
    # if not search:
    #     result.append({
    #             'title': f"Back",
    #             'subtitle': f"Back to select leagues.",
    #             'arg': 'back',
    #             'valid' : True,
    #             'icon': {
    #                 'path': f"src/back-icon.png",
    #             },
    #     }) 
    # else:
    #     result.append({
    #             'title': f"Back",
    #             'subtitle': f"Data not found.",
    #             'arg': 'back',
    #             'valid' : True,
    #             'icon': {
    #                 'path': f"src/back-icon.png",
    #             },
    #     })
    return result



"""Run Script Filter."""
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    # division = 'eng.1'
    posts  = settings(search=SEARCH)
    data = json.dumps({ "items": posts }, indent=4)
    print(data)

# def data_object(division=None):
#     fileJson = f"Cache/{division}.json"
#     f = open(fileJson)
#     posts = json.load(f)
#     return posts

if __name__ == '__main__':
    # default load filter
    main()