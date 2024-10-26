# streamlit_app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re
import json
import time
import math
from spotify_api_miner import *
from music_data_analyser import *

# Initialize session state for artists data
if 'artists' not in st.session_state:
    st.session_state.artists = {}

# Helper functions
def load_artists():
    try:
        with open("resources/artists.json", 'r') as file:
            artists = json.load(file)
            st.session_state.artists = artists if '1' in artists.keys() else {}
    except FileNotFoundError:
        st.session_state.artists = {}

def save_artists():
    with open("resources/artists.json", 'w') as file:
        json.dump(st.session_state.artists, file)

def display_artist_list():
    st.write("### Artists List")
    for nr, name in st.session_state.artists.items():
        st.write(f"**{nr}**: {name[0]}")

def plot_release_history(dates, name):
    dates.sort()
    years = list(range(int(dates[0]), int(dates[-1])))
    release_counts = [dates.count(str(year)) for year in years]
    fig, ax = plt.subplots()
    ax.plot(years, release_counts)
    ax.set_title(f'{name} Release History')
    ax.set_xlabel('Year')
    ax.set_ylabel('Release Count')
    st.pyplot(fig)

# Main Streamlit app structure
st.title("Music Data Analyzer")

# Load initial artist data
load_artists()

option = st.selectbox("Choose an option", [
    "Show List of Artists",
    "Plot Release History",
    "Analyze Artist Lyrics",
    "Compare Artists",
    "Add New Artist"
])

if option == "Show List of Artists":
    display_artist_list()

elif option == "Plot Release History":
    display_artist_list()
    artist_nr = st.text_input("Enter Artist Number:")
    if artist_nr and artist_nr in st.session_state.artists:
        spotify_data = read_release_history(artist_nr)
        release_dates = [item['release_date'][:4] for item in spotify_data['items']]
        plot_release_history(release_dates, st.session_state.artists[artist_nr][0])

elif option == "Analyze Artist Lyrics":
    display_artist_list()
    artist_nr = st.text_input("Enter Artist Number:")
    if artist_nr and artist_nr in st.session_state.artists:
        artist_name = st.session_state.artists[artist_nr][0]
        st.write(f"**Wikipedia Info for {artist_name}**")
        wiki_info = retrieve_wikipage_info(artist_name)
        st.write(f"[Open Wiki Page]({wiki_info['wiki_url']})")
        st.write(f"Total Words: {wiki_info['total_words']}")
        st.write(f"Estimated Reading Time: {wiki_info['reading_time']} minutes")

elif option == "Compare Artists":
    display_artist_list()
    artist_nr_1 = st.text_input("Enter First Artist Number:")
    artist_nr_2 = st.text_input("Enter Second Artist Number:")
    if artist_nr_1 and artist_nr_2:
        if artist_nr_1 in st.session_state.artists and artist_nr_2 in st.session_state.artists:
            artist_1_name = st.session_state.artists[artist_nr_1][0]
            artist_2_name = st.session_state.artists[artist_nr_2][0]
            st.write(f"Comparing {artist_1_name} and {artist_2_name}")
            compare_duration_artists(artist_nr_1, artist_nr_2, st.session_state.artists)

elif option == "Add New Artist":
    artist_name = st.text_input("Enter the Name of the Artist to Add:")
    if st.button("Add Artist"):
        if artist_name:
            new_artists = add_artist(artist_name, st.session_state.artists)
            if new_artists:
                st.session_state.artists = new_artists
                save_artists()
                st.success(f"{artist_name} added successfully!")
            else:
                st.error("Failed to add artist. Check internet connection.")
