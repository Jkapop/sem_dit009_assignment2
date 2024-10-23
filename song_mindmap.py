import requests
import networkx as nx
import matplotlib.pyplot as plt
import time

# Basis-URL der API
BASE_URL = "https://dit009-spotify-assignment.vercel.app/api/v1"


# Funktion zum Abrufen der Alben und Songs eines Künstlers
def get_albums_and_tracks(artist_name):
    # Anfrage, um die Artist-ID zu bekommen
    artist_search_url = f"{BASE_URL}/search?q=artist:{artist_name}&type=artist"
    print(artist_search_url)
    response = requests.get(artist_search_url)
    
    if response.status_code != 200:
        print(f"Fehler bei der Suche nach dem Künstler {artist_name}")
        return {}
    
    artist_data = response.json()
    if not artist_data:
        print(f"Kein Künstler gefunden mit dem Namen: {artist_name}")
        return {}
    
    artist_id = artist_data["artists"]["items"][0]['id']
    print(artist_id)
    
    # Anfrage für die Alben des Künstlers
    albums_url = f"{BASE_URL}/artists/{artist_id}/albums"
    print("Album URL:", albums_url)
    response = requests.get(albums_url)
    
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Alben für {artist_name}")
        return {}
    
    albums_data = response.json()
    
    album_dict = {}

    print("Wait 30 seconds")
    time.sleep(30)
    
    for album in albums_data["items"][:4]:
        print(album["id"])
        album_name = album['name']
        album_id = album['id']
        
        # Anfrage für die Tracks eines Albums
        tracks_url = f"{BASE_URL}/albums/{album_id}/tracks"
        response = requests.get(tracks_url)
        print("Tracks URL:", tracks_url)

        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Tracks für das Album {album_name}")
            continue
        if response.status_code == 439:
            print("Maximale Anzahl d. Anfragen. Warte 30 Sekunden")
            
        
        tracks_data = response.json()
        track_names = [track['name'] for track in tracks_data["items"]]
        
        album_dict[album_name] = track_names
        time.sleep(10)
    
    return album_dict

# Mindmap (Netzwerk) erstellen
def create_mindmap(artist_name):
    album_dict = get_albums_and_tracks(artist_name)
    
    if not album_dict:
        print("Keine Daten gefunden, um die Mindmap zu erstellen.")
        return
    
    # Graph erstellen
    G = nx.Graph()
    
    # Künstlername als zentraler Knoten
    G.add_node(artist_name, color='red', size=1000)  # Knoten für den Künstler

    # Verwendeter Trackset zur Vermeidung von Duplikaten
    track_set = set()

    # Knoten und Kanten für Alben und Songs hinzufügen
    for album, tracks in album_dict.items():
        G.add_node(album, color='blue', size=500)  # Knoten für jedes Album
        G.add_edge(artist_name, album)  # Kante zwischen Künstler und Album
        
        for track in tracks:
            if track not in track_set:  # Verhindere Duplikate
                G.add_node(track, color='green', size=100)  # Knoten für jeden Song
                track_set.add(track)  # Füge den Track zum Set hinzu
            
            # Verbinde das Album mit dem Song (keine Duplikate für Songs)
            G.add_edge(album, track)
    
    # Positionen für die Knoten berechnen (spring_layout für bessere Lesbarkeit)
    pos = nx.spring_layout(G, k=0.5, center=(0, 0))
    
    # Farben und Größen der Knoten vorbereiten
    node_colors = [G.nodes[node]['color'] for node in G.nodes]
    node_sizes = [G.nodes[node]['size'] for node in G.nodes]
    
    # Zeichnen der Mindmap
    plt.figure(figsize=(50, 50))
    
    # Zeichne Knoten und Kanten
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, font_color='black')

    # Verschiebe die Labels etwas, um Überlappungen zu vermeiden
    label_pos = {key: (x, y+0.02) for key, (x, y) in pos.items()}  # Anpassung des Label-Offsets
    
    # Labels zeichnen (mit leicht verschobener Position)
    nx.draw_networkx_labels(G, label_pos, font_size=10)
    
    plt.title(f'Mindmap von {artist_name}: Alben und Songs (Erste 4 Alben)')
    plt.show()

# Beispiel verwenden
artist_name = "Lady%20Gaga"
create_mindmap(artist_name)
