import sys
import requests

if len(sys.argv) < 2:
    exit("Did you really think that would work?")

with open('api.bearer', 'r') as bearer:
    btoken = bearer.read()
    btoken = f'Bearer {btoken}'

with open('flickr.key', 'r') as flickfile:
    flickey = flickfile.read()
    
headers = {'Authorization' : btoken}

tweet_id=sys.argv[1]

def getAngry(windex, debug=False):
    word = "angry"
    flickrhead = {}
    flickrhead['api_key'] = flickey
    flickrhead['safe_search'] = '1'
    flickrhead['method'] = 'flickr.photos.search'
    flickrhead['tags'] = word
    flickrhead['format'] = 'json'
    flickrhead['nojsoncallback'] = '1'
    response = requests.get("https://api.flickr.com/services/rest/", flickrhead)
    res = response.json()["photos"]

    if len(res['photo']) == 0: return None

    photos = []
    for photo in res['photo']:
        photos.append([photo['farm'], photo['server'], photo['id'], photo['secret'], photo['owner']])

    flickrhead.pop('tags')
    urls = []
    for photo in photos:
        orig = getOrigImage(photo[2])
        flickrhead['method'] = 'flickr.photos.getSizes'
        flickrhead["photo_id"] = str(photo[2])
        fresp = requests.get("https://api.flickr.com/services/rest/", flickrhead)
        temp = fresp.json()["sizes"]["size"][-1]
        if orig is not None: urls.append(temp["source"])

    #print("Got image data for", word)
    return { "word" : word, "urls": urls };

tweet_endpoint = f'https://api.twitter.com/1.1/statuses/show.json?id={tweet_id}'
res = requests.get(tweet_endpoint, headers=headers)
print(res.json())

