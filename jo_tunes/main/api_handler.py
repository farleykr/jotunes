import json
import random
import requests


with open('/etc/config.json') as config_file:
    config = json.load(config_file)

AUTH_KEY = config['HASHED_KEYS']

def get_token():
    """ Uses AUTH_KEY to get access_token """

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization':f'Basic {AUTH_KEY}',
        }
    data = {'grant_type':'client_credentials'}

    res = requests.post(url, headers=headers, data=data)

    return res.json()['access_token']


def get_playlist():
    """ Uses access_token to get playlist in json form"""

    PLAYLIST_ID = '5Cp5QIoQHhd9NtA4IIBwCb'

    token = get_token()
    url = f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}'
    headers = {
            'Accept': 'application/json',
            'Content-Type':'application/json',
            'Authorization':f'Bearer {token}'
            }

    res = requests.get(url, headers=headers)

    playlist = res.json()

    return playlist

def filter_song_data():
    """ Filters playlist info down to name and link for track and artist """

    all_tracks = dict()
    playlist = get_playlist()

    for track in playlist['tracks']['items']:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']

        track_link = track['track']['external_urls']['spotify']
        artist_link = track['track']['artists'][0]['external_urls']['spotify']
        album_art = track['track']['album']['images'][1]['url']
        
        track_info = artist_name, track_link, artist_link, album_art

        all_tracks[track_name] = track_info

    return all_tracks

def random_songs():
    """ Selects a number of random songs from entire filtered playlist 
        and makes a new playlist to be consumed by front end """

    NUMBER_OF_SONGS = 3
    songs = filter_song_data()

    get_random_keys = random.sample(songs.keys(), NUMBER_OF_SONGS)

    new_playlist = dict()

    for key in get_random_keys:
        new_playlist[key] = songs[key]
    
    return new_playlist
