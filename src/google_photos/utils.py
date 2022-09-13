from src.google_photos.build import authenticate
import json
import requests
import pandas as pd


google_photos = authenticate()

def list_albums():
    items = []
    nextpagetoken = None
    # The default number of media items to return at a time is 25. The maximum pageSize is 100.
    while nextpagetoken != '':
        print(f"Number of items processed:{len(items)}", end='\r')
        results = google_photos.albums().list(pageSize=50, pageToken=nextpagetoken).execute()
        items += results.get('albums', [])
        nextpagetoken = results.get('nextPageToken', '')
        
    # Convert the list of dict into a dataframe.
    df = pd.DataFrame(items)
    return df

def list_album_photos(album_id, size=None):
    items = []
    nextpagetoken = None
    # The default number of media items to return at a time is 25. The maximum pageSize is 100.
    while nextpagetoken != '':
        print(f"Number of items processed:{len(items)}", end='\r')
        results = google_photos.mediaItems().search(body = {
            'albumId': album_id,
            'pageSize': 50,
            'pageToken': nextpagetoken}).execute()
        items += results.get('mediaItems', [])
        nextpagetoken = results.get('nextPageToken', '')
        
    # Convert the list of dict into a dataframe.
    df = pd.DataFrame(items)
    
    if size == 'original':
        df['original_height'] = df['mediaMetadata'].apply(lambda x: x['height'])
        df['original_width'] = df['mediaMetadata'].apply(lambda x: x['width'])
        df['baseUrl'] = df.apply(lambda x: x['baseUrl'] + '=w' + x['original_width'] + '-h' + x['original_height'], axis=1)
    return df


def download_photo(photo_url, filename, destination_folder):
    response = requests.get(photo_url)
    with open(destination_folder + filename, 'wb') as f:
        f.write(response.content)
        f.close()

def upload_photo(filename, source_folder, album_id=None, service=google_photos):
    f = open(source_folder + filename, 'rb').read();
    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    headers = {
        'Authorization': "Bearer " + service._http.credentials.token,
        'Content-Type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': filename,
        'X-Goog-Upload-Protocol': "raw",
    }
    r = requests.post(url, data=f, headers=headers)
    upload_token = r.content.decode()
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
    body = {
        'newMediaItems' : [
            {
                "description": "",
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }  
            }
        ]
    }

    if album_id is not None:
        body['albumId'] = album_id;


    bodySerialized = json.dumps(body);
    headers = {
        'Authorization': "Bearer " + service._http.credentials.token,
        'Content-Type': 'application/json',
    }

    r = requests.post(url, data=bodySerialized, headers=headers)
    return r.content.decode()
