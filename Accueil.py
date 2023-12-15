import string
import streamlit as st
import pandas as pd
from WebCrawler.WebCrawler.pipelines import *
from functions import *

st.set_page_config(page_title="Spoticar Scraper", page_icon="🚙", layout="wide")

st.sidebar.markdown(
    """
    Cette application récupère les données des voitures d'occasion sur le site [Spoticar](https://www.spoticar.fr/voitures-occasion) et les affiche dans un tableau, avec différents filtres.

    Elle utilise le framework [Streamlit](https://www.streamlit.io/) pour la partie scraping, afin de collecter un volume important de données de manière efficace et structurée.
    """
)

st.sidebar.info(
    """
    👨‍💻 **Développement:** \n [Romain_Rullier](https://www.linkedin.com/in/romain-rullier-78120/)\n
    📧 **Contact:** [romain.rullier57@gmail.com](mailto:romain.rullier57@gmail.com)\n
    🌐 **Application Web:** [spoticar-scraper.app](https://spoticar-scraper.streamlit.app/)\n
    📄 **GitHub Projet:** [RomainRullier](https://github.com/RomainRullier/Spoticar-Scraper)
    """
)


st.subheader("Récupérateur de données Spoticar")

if 'historique_collectes' not in st.session_state:
    st.session_state['historique_collectes'] = []

# Filtrer les voitures par lettre
alphabet = list(string.ascii_uppercase)
alphabet.insert(0, "Tout")
selected_letter = st.selectbox("Filtrer par lettre", alphabet)

# Filtrer les voitures par prix
prix_min, prix_max = st.slider("Filtrer par prix (en €)", 1000, 200000, (1000, 200000))

# Filtrer les voitures par année

# Bouton pour lancer la collecte de données
if st.button("Lancer la collecte de données"):
    try:
        # Lancement de la collecte de données
        start_scraping()

        # Récupération et filtrage des données
        database = DataBase('spoticar')
        all_voitures = database.select_table('spoticar')
        voitures_filtered_by_letter = get_voitures_by_letter(all_voitures, selected_letter)
        voitures_filtered = get_voitures_by_price(voitures_filtered_by_letter, (prix_min, prix_max))

        # Enregistrer la collecte dans l'historique
        st.session_state['historique_collectes'].append({
            "data": voitures_filtered,
            "filtres": {"lettre": selected_letter, "prix_min": prix_min, "prix_max": prix_max}
        })

        st.session_state['data'] = voitures_filtered

        st.success("La collecte de données a été effectuée avec les filtres appliqués !")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la collecte de données : {e}")


# Afficher un bouton pour télécharger les données
if 'data' in st.session_state and st.session_state['data']:
    df = pd.DataFrame(st.session_state['data'])
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
