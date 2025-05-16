import streamlit as st
import requests

# Configuration de l'URL du backend
API_URL = "http://127.0.0.1:8000"

# Titre de l'application
st.title("🎬 Movie Explorer")

# Initialiser les variables de session si elles n'existent pas encore
if "current_movie" not in st.session_state:
    st.session_state.current_movie = None

if "summary" not in st.session_state:
    st.session_state.summary = ""

# Bouton pour afficher un film aléatoire
if st.button("🎲 Show Random Movie"):
    try:
        response = requests.get(f"{API_URL}/movies/random/")
        response.raise_for_status()
        movie = response.json()

        # Stocker le film dans la session
        st.session_state.current_movie = movie
        st.session_state.summary = ""  # Réinitialiser le résumé

    except requests.RequestException as e:
        st.error(f"Erreur lors de la récupération du film : {e}")

# Affichage des détails du film si disponible
movie = st.session_state.current_movie

if movie:
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"🎬 Directed by: {movie['director']}")

    st.subheader("Actors")
    for actor in movie["actors"]:
        st.write(f"🎭 {actor['actor_name']}")

    # Bouton pour générer le résumé (activé uniquement si un film est chargé)
    if st.button("🧠 Get Summary"):
        try:
            payload = {"movie_id": movie["id"]}
            response = requests.post(f"{API_URL}/generate_summary/", json=payload)
            response.raise_for_status()
            summary_data = response.json()

            # Stocker le résumé dans la session
            st.session_state.summary = summary_data["summary_text"]


        except requests.RequestException as e:
            st.error(f"Erreur lors de la génération du résumé : {e}")

    # Afficher le résumé s’il existe
    if st.session_state.summary:
        st.subheader("📝 Summary")
        st.info(st.session_state.summary)



