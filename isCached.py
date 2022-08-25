import json
import requests
import pathlib
from datetime import datetime
import os

#make dir cache
pathlib.Path('Cache').mkdir(parents=True, exist_ok=True) 

## variables
time_format = "%Y-%m-%d %H:%M:%S"
fileJson = 'Cache/isCached.json'
parse_time_now = datetime.now()
time_now = parse_time_now.strftime(time_format)
# cache_time = 8 #hours
baseUrl = 'https://api-football-standings.azharimm.site/leagues/'
data_year = os.environ['data_year']
# data_year = '2020'

class doCache:
    
    @staticmethod
    def compare_time(dataId=None, cache_time=2):
            
            d1 = datetime.strptime(get_time_value(dataId), time_format)
            d2 = datetime.strptime(time_now, time_format)
            
            daysDiff = (d2-d1).days
            hoursDiff = daysDiff * 24
            
            if get_data_year(dataId) != data_year or hoursDiff > cache_time:
                write_time(dataId)
                save_data(dataId)
                return True
            else:
                return False
            
def write_time(dataId=None):
            with open(fileJson, 'r') as f:
                my_list = json.load(f)
                for idx, obj in enumerate(my_list):
                    if obj['id'] == dataId:
                        obj['last_updated'] = time_now
                        obj['data_year'] = data_year
                        
            with open(fileJson, 'w') as f:
                f.write(json.dumps(my_list, separators=(',',': '), indent=4))
            return
        
def save_data(dataId=None):
        if (dataId == 'leagues'):
            jsonInternet = requests.get(baseUrl) # (json url)
        else:
            jsonInternet = requests.get(f"{baseUrl}{dataId}/standings?season={data_year}&sort=asc") # (json url)
        data = jsonInternet.json()
        with open(('Cache/'+dataId+'.json'), 'w') as f:
            json.dump(data, f, indent=4, separators=(',',': '))
        
        # write_time(dataId)
                
def get_time_value(dataId=None):
        with open(fileJson) as f:
            data = json.load(f)
            list1 = list ((p_id.get('last_updated') for p_id in data if p_id.get('id') == dataId)) 
            return ''.join(list1)
        
def get_data_year(dataId=None):
        with open(fileJson) as f:
            data = json.load(f)
            list1 = list ((p_id.get('data_year') for p_id in data if p_id.get('id') == dataId)) 
            return ''.join(list1)

# save_data("eng.1")
# be = doCache()
# print(be.compare_time("eng.1"))



