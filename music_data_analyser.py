import matplotlib.pyplot as plt
import numpy as np
import re
import requests
import json
from spotify_api_miner import *
import time

# Print imported artists
def print_artists(artists):
    print("-----------------------------------------------")
    print(f"{'Artist Nr.':<10}{'Artist Name':>30}")
    print("-----------------------------------------------")
    for nr, name in artists.items():
        print(f"{nr:<10}{name[0]:>30}")
    print("-----------------------------------------------")

# Load a dictionary containing the top 10 songs from an artist from a .json file
def get_top(artist_nr):  
    try:
        filename = "./top_"+artist_nr+".json"
        with open(filename, 'r') as file:
            top_data = json.load(file)
        return top_data
    except:
        print("A file is missing. Add artist again to retrieve their top songs.")

# Get charts:
def get_charts():
    try: # Check whether charts.json is in directory
        with open("./charts.json", 'r') as file:
            charts = json.load(file)
            return charts
    except: # If file is not in directory: Retrieve it through API
        try:
            charts = retrieve_charts()
            return charts
        except: 
            print("Charts could not be accessed. Check your internet connection")
            return None


# Load the song features (danceability,...) of a list of songs from .json file or API
def get_features(artist_nr, id_list):       
    filename = "./features_"+artist_nr+".json"
    with open(filename, 'r')as file:
        audio_features = json.load(file)
    return audio_features
 

def get_release_history(id, artist_nr):    
    filename = "./release_history_"+artist_nr+".json"
    with open(filename, 'r')as file:
        audio_features = json.load(file)
    return audio_features

def plot_release_history(dates) :
    dates.sort()
    print(dates)
    xpoints = []
    ypoints = []
    for i in range(len(dates)) :
        if dates[i] in xpoints :
            j = 0
            done = False
            while j < len(xpoints) and not done :
                if dates[i] == xpoints[j] :
                    ypoints[j] += 1
                    done = True
                j += 1
        else :
            xpoints.append(dates[i])
            ypoints.append(1)

    plt.plot(np.asarray(xpoints), np.asarray(ypoints))
    plt.title('Release history')
    plt.xlabel('Year')
    plt.ylabel('Release count')
    plt.show()

def get_release_dates_of_artist(data) :
    releases = []
    for album in range(len(data['items'])) :
        date = data['items'][album]['release_date']
        releases.append(date[:4])
    return releases

def get_explicit_percent(data) : # make this recursive for extra credit?
    expl_count = 0
    for song in data['tracks']['items'] :
        print(song['track']['explicit'])
        if song['track']['explicit'] == True :
            expl_count += 1
    return (expl_count / len(data['tracks']['items']))* 100
    
def are_lyrics_personal() :
    artist_name = input("Please input an artist name to analyze their lyrics: ")
    track = input("Please input one of their songs: ")
    try:
        lyr_response = retrieve_lyrics(artist_name, track)
    except: 
        print("Internet connection failed.") 
        return None
    if lyr_response == {'error': 'No lyrics found'}:
        print("This song was not found.")
    else:    
        lyrics_data = lyr_response['lyrics']

        me_list = re.findall(r"I|me|mine", lyrics_data)
        they_list = re.findall(r"he|him|she|her|they|them", lyrics_data)
        you_list = re.findall(r"you|your|yours", lyrics_data)

        # absolutely ATROCIOUS code by aupra. awful practice!
        if len(me_list) > len(you_list) and len(me_list) > len(they_list) : # me
            print(f"{track} by {artist_name} is a selfish song, all about 'me'!")
        elif len(you_list) > len(me_list) and len(you_list) > len(they_list) : # you
            print(f"{track} by {artist_name} is a song all about 'you'!")
        elif len(they_list) > len(me_list) and len(they_list) > len(you_list) : # they
            print(f"{track} by {artist_name} mentions other people a lot.")
        if len(me_list) == len(you_list) and len(me_list) > len(they_list) : # me you
            print(f"{track} by {artist_name} is equally about 'you' and 'me'. Lovely!")
        elif len(you_list) == len(they_list) and len(you_list) > len(me_list) : # you they
            print(f"{track} by {artist_name} is all about 'you' and other people.")
        elif len(they_list) == len(me_list) and len(they_list) > len(you_list) : # me they
            print(f"{track} by {artist_name} talks about the singer and people around them equally.")
        elif len(they_list) == len(me_list) == len(you_list) : # me you they
            print(f"{track} by {artist_name} is truly a song about everyone :)")

        buckets = [len(me_list), len(you_list), len(they_list)]
        plt.bar(["I", "You", "They"], buckets)
        plt.show()

# Compare the average duration of top 10 songs from two artists
def compare_duration(artist_nr_1, artist_nr_2, artists_dict):
    top_data_1 = get_top(artist_nr_1)
    top_data_2 = get_top(artist_nr_2)
    artist_name_1 = artists_dict[artist_nr_1][0]
    artist_name_2 = artists_dict[artist_nr_2][0]
    top_data_1 = top_data_1['tracks']
    top_data_2 = top_data_2['tracks']
    duration_artist_1 = []
    duration_artist_2 = []
    for song in top_data_1:
        duration = song['duration_ms']
        duration_artist_1.append(duration)
    for song in top_data_2:
        duration = song['duration_ms']
        duration_artist_2.append(duration)

    total_duration_1 = 0
    for song in duration_artist_1:
        total_duration_1 += song/1000
    mean_duration_1 = int(total_duration_1 / 10)
    minutes_1 = mean_duration_1 // 60
    seconds_1 = mean_duration_1 % 60
    print(f"Average duration of Top 10 {artist_name_1} Songs: {minutes_1}:{seconds_1:02d} minutes")

    total_duration_2 = 0
    for song in duration_artist_2:
        total_duration_2 += song/1000
    mean_duration_2 = int(total_duration_2 / 10)
    minutes_2 = mean_duration_2 // 60
    seconds_2 = mean_duration_2 % 60
    print(f"Average duration of Top 10 {artist_name_2} Songs: {minutes_2}:{seconds_2} minutes")

    if mean_duration_1 > mean_duration_2:
        duration_ratio = total_duration_1 / total_duration_2
        print(f"{artist_name_1}'s songs are on average {duration_ratio:.2f} times longer")
    elif mean_duration_1 < mean_duration_2:
        duration_ratio = total_duration_2 / total_duration_1
        print(f"{artist_name_2}'s songs are on average {duration_ratio:.2f} times longer")
    else: print(f"The songs of {artist_name_1} and {artist_name_2} have on average the same duration!")

# Calculate how pop-py an artist is (based on popularity, danceability and duration of top 10 songs)    
def calculate_pop_index(artist_nr):
    top_tracks = get_top(artist_nr)
    id_list = []
    for song in top_tracks['tracks']:
        id_list.append(song['id'])
    audio_features = get_features(artist_nr, id_list)
    mean_popularity = 0
    mean_danceability = 0
    mean_duration = 0
    for song in top_tracks['tracks']:
        mean_popularity += (song['popularity'] / 100)
        mean_duration += (song['duration_ms'] /100000)
    mean_popularity /= 10
    mean_duration /= 10
    for song in audio_features['audio_features']:
        mean_danceability += song['danceability']
    mean_danceability /= 10
    pop_index = mean_popularity * mean_danceability / (mean_duration)**0.5
    return pop_index

def main() :
    # Import artists from .json file (if file does not exist: create dictionary with two artists)
    # Format of dictionary 'artists': 
    # keys -> artist numbers (starting at 1)
    # values -> list with Name of Artist (index:[0]) and ID of artist (index:[1])
    try:
        with open("./artists.json", 'r')as file:
            artists = json.load(file)
    except: artists = {"1": ["Lady Gaga", "1HY2Jd0NmPuamShAr6KMms"], "2": ["Porcupine Tree", "5NXHXK6hOCotCF8lvGM1I0"]}
    
    option = ""
    query = """
    Type "exit" to leave program (and to save added artists for future use)
    Type 0 to show list of artists
    Type 1 to plot the release history of an artist.
    Type 2 to check how personal a song's lyrics are.
    Type 3 to check how explicit the top songs are.
    Type 4 for smth with the Wikipedia API
    Type 5 to compare the average song duration of artists
    Type 6 to calculate the POP-INDEX of an artist
    Type x to add an artist (requires internet connection and takes up to 50 seconds)
"""
    while option != "exit" :
        print(query)
        option = input()
        match option :
            case "0": 
                print_artists(artists)
            
            case "1" : # artist's release history
                print_artists(artists)
                artist_nr = input("Artist Nr: ")
                if artist_nr in artists.keys():    
                    try:
                        id = artists[artist_nr][1]
                        spotify_data = get_release_history(id ,artist_nr)
                        release_dates = get_release_dates_of_artist(spotify_data)
                        plot_release_history(release_dates)
                    except: print("An error occured. Check your internet connection.")
                else:
                    print("Artist number not available. Try again.")

            case "2" : # how personal lyrics are
                are_lyrics_personal()

            case "3" : # explicity check    
                spotify_data = get_charts()
                expl = get_explicit_percent(spotify_data)
                print(f"This week's top hits playlist is {expl}% explicit.")

            case "4" : # wikipedia or whatever
                # we need to have another task with a different api - wikipedia API seems somewhat simple and good to use,
                # and lots of data
                pass

            case "5" : # Compare the average song length (Top 10) of two artists
                print_artists(artists)
                artist_nr_1 = input("Artist Nr 1: ")
                artist_nr_2 = input("Artist Nr 2: ")
                if artist_nr_1 in artists.keys() and artist_nr_2 in artists.keys():
                    compare_duration(artist_nr_1, artist_nr_2, artists)
                else: print("At least one of the artist numbers does not exist. Try again.")

            case "6": # Calculate POP-Index of an artist
                print_artists(artists)
                artist_nr = input("Enter artist number:")
                if artist_nr in artists.keys():
                    pop_index = calculate_pop_index(artist_nr)
                    print(f"{artists[artist_nr][0]} has a POP-Index of {pop_index:.2f}")
                else: print("Artist number not available. Try again.")
            
            case "x": # Add artist
                name = input("Name of artist you want to add:")
                try:
                    id = retrieve_artist_id(name)
                    new_key = str(int(max(artists.keys()))+1)                  
                    top_tracks = retrieve_top_tracks(new_key, id)
                    retrieve_release_history(id, new_key)
                    id_list = []
                    for song in top_tracks['tracks']:
                        id_list.append(song['id'])
                    print("Wait 30 seconds - due to limited requests to spotfy API")
                    time.sleep(30)
                    retrieve_audio_features(id_list, new_key)
                    artists.update({new_key : [name, id]})
                except: 
                    print("An error occured. Check your internet connection.")

            case "exit" :
                with open("./artists.json", 'w') as file:
                    json.dump(artists, file)
                print("bye bye!")
            
            case _ :
                print("Invalid input, try again!")

if __name__ == "__main__" :
    main()