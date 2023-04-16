import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import webbrowser

def generate_playlist(genre, duration, popularity):
    # Lê o conteúdo do arquivo id.txt e armazena na variável client_id
    with open("id.txt", "r") as file:
        id = file.read().strip()

    # Lê o conteúdo do arquivo secret.txt e armazena na variável client_secret
    with open("secret.txt", "r") as file:
        secret = file.read().strip()

    # Autenticação
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=id, client_secret=secret, redirect_uri='http://localhost:8888/callback'))

    # Processamento de dados
    track_ids = []
    offset = 0
    while len(track_ids) < 100:
        results = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=offset, market="US")
        tracks = results["tracks"]["items"]
        tracks_sorted = sorted(tracks, key=lambda t: t["popularity"], reverse=True)
        for track in tracks_sorted:
            if track["popularity"] >= popularity:
                track_ids.append(track["id"])
        offset += 50
        if offset >= 2000:
            break

    # Criação da Playlist
    playlist_name = f"{genre} Playlist"
    new_playlist = sp.user_playlist_create(user=sp.me()["id"], name=playlist_name, public=True)

    # Adicionar faixas à playlist até que a duração total desejada seja alcançada ou ultrapassada
    duration_sum = 0
    var_count = 0
    playlist_tracks = []

    for track_id in track_ids:
        track_info = sp.track(track_id)
        if duration_sum + track_info['duration_ms'] <= duration * 60000:
            sp.playlist_add_items(playlist_id=new_playlist["id"], items=[track_info['uri']])
            playlist_tracks.append(track_info['uri'])
            duration_sum += track_info['duration_ms']
            var_count += 1

        if duration_sum >= duration * 60000:
            break

    # Exibição dos resultados
    print(f"A playlist '{playlist_name}' foi criada com sucesso!")
    print(f"Foram adicionadas {var_count} músicas, com duração total de {round(duration_sum / 60000, 2)} minutos.")
    time.sleep(1)
    print("Abrindo a playlist no Spotify...")
    time.sleep(1)
    webbrowser.open(new_playlist['external_urls']['spotify'])
