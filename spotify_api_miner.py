import requests
import json

# Get release history of an artists (based on artist ID)
def retrieve_release_history(id, artist_nr):
    songs = "/artists/"+id+"/albums"        
    url = f"https://dit009-spotify-assignment.vercel.app/api/v1{songs}"
    response = requests.get(url)
    spotify_data = response.json()
    filename = "./resources/release_history_"+artist_nr+".json"
    with open(filename, 'w') as file:
        json.dump(spotify_data, file)
    return spotify_data

# Get the Top 10 tracks of an artist (based on asrtist ID)
def retrieve_top_tracks(artist_nr, artist_id):
    top_url = "https://dit009-spotify-assignment.vercel.app/api/v1/artists/"+artist_id+"/top-tracks" 
    top_response = requests.get(top_url)
    top_data = top_response.json()
    filename = "./resources/top_"+artist_nr+".json"
    with open(filename, 'w') as file:
        json.dump(top_data, file)
    return top_data

def retrieve_charts():
    url = f"https://dit009-spotify-assignment.vercel.app/api/v1/playlists/37i9dQZEVXbNG2KDcFcKOF"
    response = requests.get(url)
    spotify_data = response.json()
    with open("./resources/charts.json", 'w') as file:
        json.dump(spotify_data, file)
    return spotify_data

# Get the audio features (danceability,...) for a list of songs (based on song IDs)
def retrieve_audio_features(id_list, artist_nr):
    features_url = "https://dit009-spotify-assignment.vercel.app/api/v1/audio-features?ids="
    for id in id_list:
        features_url += id + "%2C"
    features_response = requests.get(features_url)
    features_data = features_response.json()
    filename = "./resources/features_"+str(artist_nr)+".json"
    with open(filename, 'w') as file:
        json.dump(features_data, file)
    return features_data

# Use Spotify's search function to get the ID for an artist (based on user input for artist name)
def retrieve_artist_id(name):
    name = name.split()
    if len(name)== 0:return ""
    elif len(name) == 1:
        search_url = "https://dit009-spotify-assignment.vercel.app/api/v1/search?q=artist:"+name[0]+"&type=artist"
    else:
        artist_string = name[0]
        for i in range(1, len(name)):
            artist_string += "%20"+name[i]
        search_url = "https://dit009-spotify-assignment.vercel.app/api/v1/search?q=artist:"+artist_string+"&type=artist" 
    id_response = requests.get(search_url)
    id_data = id_response.json()     
    id = id_data['artists']['items'][0]['id']
    actual_name = id_data['artists']['items'][0]['name']
    return id, actual_name

# Lyrics API: Get lyrics for a song (based on artist name and title)
def retrieve_lyrics(artist_name, track):
    lyrics_url = f"https://api.lyrics.ovh/v1/{artist_name}/{track}"
    lyr_response = requests.get(lyrics_url)
    lyr_data = lyr_response.json()
    return lyr_data