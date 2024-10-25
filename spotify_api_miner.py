import requests
import json
import datetime
import re

# Spotify API: Get release history of an artists (based on artist ID)
def retrieve_release_history(id, artist_nr):
    songs = "/artists/"+id+"/albums"        
    url = f"https://dit009-spotify-assignment.vercel.app/api/v1{songs}"
    response = requests.get(url)
    spotify_data = response.json()
    filename = "./resources/release_history_"+artist_nr+".json"
    with open(filename, 'w') as file:
        json.dump(spotify_data, file, indent=4)
    return spotify_data

# Spotify API: Get the Top 10 tracks of an artist (based on asrtist ID)
def retrieve_top_tracks(artist_nr, artist_id):
    top_url = "https://dit009-spotify-assignment.vercel.app/api/v1/artists/"+artist_id+"/top-tracks" 
    top_response = requests.get(top_url)
    top_data = top_response.json()
    filename = "./resources/top_"+artist_nr+".json"
    with open(filename, 'w') as file:
        json.dump(top_data, file, indent=4)
    return top_data

# Spotify API: Get the charts
def retrieve_charts():
    url = f"https://dit009-spotify-assignment.vercel.app/api/v1/playlists/37i9dQZEVXbNG2KDcFcKOF"
    response = requests.get(url)
    spotify_data = response.json()
    with open("./resources/charts.json", 'w') as file:
        json.dump(spotify_data, file, indent=4)
    return spotify_data

# Spotify API: Get the audio features (danceability,...) for a list of songs (based on song IDs)
def retrieve_audio_features(id_list, artist_nr):
    features_url = "https://dit009-spotify-assignment.vercel.app/api/v1/audio-features?ids="
    for id in id_list:
        features_url += id + "%2C"
    features_response = requests.get(features_url)
    features_data = features_response.json()
    filename = "./resources/features_"+str(artist_nr)+".json"
    with open(filename, 'w') as file:
        json.dump(features_data, file, indent=4)
    return features_data

# Spotify API: Use Spotify's search function to get the ID for an artist (based on user input for artist name)
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

# Wikipedia API: views of article
def retrieve_wikipage_views_month(search_title, print_errors = True):
    search_title = search_title.replace(" ", "_")
    date_today = datetime.datetime.today()
    formatted_date_today = date_today.strftime('%Y%m%d')
    date_30_days_ago = date_today - datetime.timedelta(days=30)
    wikistats_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{search_title}/daily/{date_30_days_ago.strftime('%Y%m%d')}/{formatted_date_today}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(wikistats_url, headers=headers)
    
    # Error handling if artist not found and API problems
    if response.status_code == 404:
        if print_errors == True: print(f"Error! Artist not found. Check spelling and try again.")
        return
    try:
        wikipedia_view_data = response.json()
    except:
        print("An error occured, please try again.")
        return

    return wikipedia_view_data

# Wikipedia API: article length
def retrieve_wikipage_info(search_title):
    query = search_title.replace(" ", "%20")
    search_url = f"https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles={query}&redirects=true"
    
    response = requests.get(search_url)

    html_content = response.text
    clean_text = re.sub(r'&lt;.*?&gt;|<.*?>', '', html_content)
    clean_text = clean_text.replace("HTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Special:MyLanguage/Extension:TextExtracts#Caveats.\n", "")

    number_words = len(clean_text.split(" "))

    info_dict = {}
    info_dict["total_words"] = number_words
    info_dict["reading_time"] = round(number_words / 280, 2)
    info_dict["wiki_url"] = f"https://en.wikipedia.org/wiki/{search_title.replace(' ', '_')}"
    
    return info_dict