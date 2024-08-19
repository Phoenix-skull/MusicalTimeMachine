# from pprint import pprint
import json


import requests
import spotipy
from requests import HTTPError
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()


with open(".cache") as file:
    access_token = json.load(file)["access_token"]


refresh_url = "https://accounts.spotify.com/api/token"
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

try:
    sp = spotipy.client.Spotify(auth=access_token, auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-private",
        show_dialog=True
    )
                         )
    user_id = sp.current_user()["id"]
    print("Successful@")
except SpotifyException or HTTPError:
    sp_auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-private",
        show_dialog=True,
    )
    with open(".cache") as cache:
        refresh_token = json.load(cache)["refresh_token"]
        access_token = sp_auth.refresh_access_token(refresh_token)
        print(access_token)
    sp = spotipy.client.Spotify(auth=access_token, auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-private",
    )
                         )
    user_id = sp.current_user()["id"]

    print("Successful")


#
#

#
#
URL = "https://www.billboard.com/charts/hot-100/"
travel_year = input("What year you would like to travel to: ")
travel_month = input("What month of that year you would like to travel to: ")
travel_day = input("What day of that month you would like to travel to: ")
travel_time = f"{travel_year}-{travel_month}-{travel_day}"
songs = requests.get(f"{URL}{travel_time}").text
soup = BeautifulSoup(markup=songs, parser="html.parser", features="lxml")
song_titles = [song_title.text.strip() for song_title in soup.find_all(name="h3", class_="a-no-trucate")]
track_ids = []

for track in song_titles:
    track_id = sp.search(q=track[0], limit=1, type="track")["tracks"]["items"][0]["uri"]
    track_ids.append(track_id)

new_playlist = sp.user_playlist_create(user=user_id, name=f"{travel_time} Billboard 100",
                                       public=False, collaborative=False,
                                       description=f'A nostalgic playlist taking you back to {travel_time} '
                                        )
new_playlist_id = new_playlist["uri"]
sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=track_ids)

