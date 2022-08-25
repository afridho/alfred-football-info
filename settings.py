import json

fileJson = f"src/settings.json"

def data_settings():
    f = open(fileJson)
    posts = json.load(f)
    return posts

def mark_favorite_club(clubName=None, clubId=None, division=None):
    with open(fileJson, 'r') as f:
                my_list = json.load(f)
                if len(clubId) == 0:
                    my_list['favorite_club'] = ''
                    my_list['favorite_club_id'] = ''
                    my_list['favorite_club_league_code'] = ''
                else:
                    my_list['favorite_club'] = clubName
                    my_list['favorite_club_id'] = clubId
                    my_list['favorite_club_league_code'] = division
                        
    with open(fileJson, 'w') as f:
        f.write(json.dumps(my_list, separators=(',',': '), indent=4))
    return  