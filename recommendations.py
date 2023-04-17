import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import webbrowser
import time
from collections import Counter

def generate_with_recommendations(duration):
    # Lê o conteúdo do arquivo id.txt e armazena na variável client_id
    with open("id.txt", "r") as file:
        id = file.read().strip()

    # Lê o conteúdo do arquivo secret.txt e armazena na variável client_secret
    with open("secret.txt", "r") as file:
        secret = file.read().strip()

    # Autenticação com o Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                                client_secret=secret,
                                                redirect_uri="http://localhost:8888/callback",
                                                scope="user-library-read playlist-modify-public user-read-recently-played"))

    # Get the user's top artists
    top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')

    # Get the genres of each artist
    genres = []
    for artist in top_artists['items']:
        artist_info = sp.artist(artist['uri'])
        genres.extend(artist_info['genres'])

    # Get the top 5 most common genres
    top_genres = [genre for genre, count in Counter(genres).most_common(5)]


    # Converter a lista de gêneros para uma lista de strings contendo apenas os nomes dos gêneros
    seed_genres = top_genres

    # Recomendar músicas com base nos gêneros encontrados
    recommendations = sp.recommendations(seed_genres=seed_genres, limit=50)


    # Criação de uma nova playlist
    playlist_name = f"Recommendations {datetime.date.today()}"
    playlist_description = f"Playlist de recomendações gerada em {datetime.datetime.now()}"
    playlist = sp.user_playlist_create(user=sp.me()["id"], name=playlist_name, public=True, description=playlist_description)

    # Adicionar faixas à playlist até que a duração total desejada seja alcançada ou ultrapassada
    duration_sum = 0
    var_count = 0
    for track in recommendations['tracks']:
        # Obter o ID da faixa
        track_id = track['id']

        # Obter a duração da faixa em minutos
        duration_min = track['duration_ms'] / 1000 / 60

        # Verificar se a duração total desejada foi alcançada
        if duration_sum + duration_min > duration:
            break

        # Adicionar a faixa à playlist
        sp.playlist_add_items(playlist_id=playlist['id'], items=[track_id])

        # Adicionar a duração da faixa à soma total
        duration_sum += duration_min
        var_count += 1




    # Exibição dos resultados
    print(f"A playlist '{playlist_name}' foi criada com sucesso!")
    print(f"Foram adicionadas {var_count} músicas, com duração total de {round(duration_min)} minutos.")
    time.sleep(1)
    print("Abrindo a playlist no Spotify...")
    time.sleep(1)
    webbrowser.open(playlist['external_urls']['spotify'])
