import streamlit as st
import pandas as pd
import requests
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

def main():

    # Fonction pour appeler l'API et obtenir les résultats d'autocomplétion
    def get_autocompletion(query):
        url = "https://api-adresse.data.gouv.fr/search/"
        params = {
            "q": query,
            "limit": 10,  # Limite le nombre de suggestions retournées
            "autocomplete": 1,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['features']
        else:
            st.error("Erreur lors de la récupération des données de l'API.")
            return []
        
    # Fonction pour obtenir les coordonnées géographiques via Geopy
    def get_coordinates(address):
        geolocator = Nominatim(user_agent="geo_locator_app", timeout=10)

        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None

    
    # Interface Streamlit
    st.set_page_config(
        page_title="GeoBAN",
        page_icon="🐋",
        #layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            
            'About': "Cette application permet de tester l'autocomplétion d'une adresse saisie grâce à la BAN, et de la géolocaliser."
        }
    )
    st.title("Autocomplétion et géolocalisation")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    Cette application permet de rechercher une adresse dans la BAN, d'obtenir des suggestions d'adresses avec un score de similarité, puis de visualiser les coordonnées géographiques sur une carte.
    
    ### Comment ça marche ?
    1. **Saisir une adresse** : la présence d'un code postal impact grandement la qualité des résultats. Les fautes d'orthographes sont permises tant qu'il y a un code postal.
    2. **Sélectionner une adresse** : après avoir saisi une adresse, une liste de suggestions apparaîtra. Choisissez celle qui possède le meilleur score.
    3. **Afficher la carte** : une fois l'adresse sélectionnée, une carte interactive s'affichera avec la position géographique de l'adresse. Vous pouvez choisir parmi plusieurs styles de carte.
    """)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Zone de texte pour l'adresse
    adresse_query = st.text_input("Recherchez une adresse:")

    # Variable pour stocker les suggestions
    suggestions = []

    # Si une adresse est entrée, on appelle l'API et on met à jour les suggestions
    if adresse_query:
        suggestions = get_autocompletion(adresse_query)
        
        if suggestions:
            # Extraire les adresses et les scores dans une liste pour la selectbox
            adresse_labels = [f"{suggestion['properties']['label']} (Score: {suggestion['properties']['score']:.2f})" for suggestion in suggestions]

            # Afficher la liste des suggestions dans un selectbox
            selected_address = st.selectbox("Sélectionnez une adresse:", adresse_labels)

            clean_address = selected_address.split('(')[0].strip()

            # Afficher l'adresse sélectionnée
            if clean_address:
                st.write(f"Adresse sélectionnée : {clean_address}")
                lat, lon = get_coordinates(clean_address)

                if lat and lon:
                    # Options de tuiles
                    tiles_option = st.selectbox("Choisissez un style de carte:", 
                                                ["OpenStreetMap",
                                                 "CartoDB dark_matter", 
                                                 "CartoDB Voyager",
                                                 "CartoDB positron", 
                                                 "Esri WorldImagery", 
                                                 "Esri WorldStreetMap", 
                                                  
                                                 "OpenTopoMap"])
                    # Créer la carte avec Folium
                    m = folium.Map(location=[lat, lon], zoom_start=15, tiles=tiles_option)
                    # Marqueur de l'adresse
                    folium.Marker([lat, lon], popup=f"Adresse : {clean_address}").add_to(m)

                    # Afficher la carte dans Streamlit
                    st_folium(m, width=700, height=500)

        else:
            st.write("Aucune suggestion trouvée.")


if __name__ == "__main__":
    main()
