import pathlib
import time
import requests
requests.packages.urllib3.disable_warnings()
from PIL import Image, UnidentifiedImageError
import os, os.path
# from PIL import

baseUrl = 'https://api-football-standings.azharimm.site/leagues/'
parent_folder_logo = 'src/team-icons/'

def get_data_from_internet(url=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    response = requests.request("GET", url, headers=headers, verify=False)
    posts = response.json()
    return posts


def get_logo(dataId=None, dataUrl=None, otherParam=None,club=True):
    if (club):
        url_logo = f"{baseUrl}{dataId}/standings?season=2022&sort=asc"
        jsonFile = get_data_from_internet(url_logo)
        
        if 'standings' in jsonFile['data']:
            posts = jsonFile['data']['standings']
            for post in posts: 
                if 'logos' in post['team'].keys(): #skip if no logo
                    URL = post['team']['logos'][0]['href'] 
                    response = requests.get(URL) if 'logos' in post['team'].keys() else None
                    open(('{}{}/{}.png'.format(parent_folder_logo, dataId, post['team']['abbreviation'])), "wb").write(response.content)
                    print(f"Filename : {post['team']['abbreviation']}.png")
                else:
                    print (f"No-logo ({post['team']['displayName']})")
            compress_png(dataId)
            print('\n') #give one line
        else:
            print('No Data Available for '+dataId+'\n')
    else:
        URL = dataUrl.rstrip('\"') #make sure to clean url
        response = requests.get(URL)
        open((f"{parent_folder_logo}{dataId}/{dataId}_{otherParam}.png"), "wb").write(response.content)
        
def compress_png(dataId=None):
    img_gallery_path = (f"{parent_folder_logo}{dataId}/")
    dir = os.listdir(img_gallery_path)
    if len(dir) != 0:
        print('Compressing image...')
        path = img_gallery_path
        valid_images = [".png",".jpeg"]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            name = os.path.splitext(f)[0]
            if ext.lower() not in valid_images:
                continue
            try:
                img=Image.open(os.path.join(path,f))
                newImage = img.resize((128, 128), Image.Resampling.LANCZOS) 
                newImage.save(img_gallery_path+name+ext.lower(),quality=0,optimize=True)
            except UnidentifiedImageError:
                continue
        print('Image Compressed.') 
        

def download():
    start_time = time.time()
    get_competition_name = get_data_from_internet(baseUrl)
    
    print('\nBegin updating logo...')
    time.sleep(0.7)
    print(f"Folder location : {parent_folder_logo}\n")
    time.sleep(0.5)
    posts = get_competition_name['data']
    for league in posts:
        pathlib.Path(f"{parent_folder_logo}{league['id']}").mkdir(parents=True, exist_ok=True)
        get_logo(league["id"],league["logos"]["light"], 'light', False)
        get_logo(league["id"],league["logos"]["dark"], 'dark', False)
        print(f"Filename : {league['id']}.png")
        
    # get from file Cached 
    # fileJson = 'Cache/isCached.json'
    # f = open(fileJson)
    # posts = json.load(f)
    
    # posts = [{'id' : 'eng.1'},{'id' : 'uga.1'}]
    
    print('\nBegin updating club logo...')
    time.sleep(0.7)
    
    """Download club logo"""
    for data in posts:
        pathlib.Path(f"{parent_folder_logo}{data['id']}").mkdir(parents=True, exist_ok=True)
        print(f"[Name : {data['name']}]") if 'name' in data else ''
        print(f"Folder : {data['id']}")
        get_logo(data["id"], None, None, True)
        time.sleep(0.5)
    
    print("--- Logo Updated %s seconds ---" % round((time.time() - start_time), 2))
    
if __name__ == '__main__':
    download()