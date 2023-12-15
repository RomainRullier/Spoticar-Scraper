import streamlit as st
import pandas as pd

st.subheader("Historique des collectes")

# Utiliser l'historique des collectes
if 'historique_collectes' in st.session_state:
    for collecte in reversed(st.session_state['historique_collectes']):
        data = collecte['data']
        filtres = collecte['filtres']

        st.write("##### Filtres appliqués")

        st.write(f"Lettre: {filtres['lettre']}, Prix Min: {filtres['prix_min']}, Prix Max: {filtres['prix_max']}")

        df = pd.DataFrame(data)
        st.dataframe(df)
else:
    st.write("Aucune donnée n'a été collectée pour le moment.")
