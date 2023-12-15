import base64
from WebCrawler.WebCrawler.pipelines import *
import subprocess

database = DataBase('spoticar')
voitures = database.select_table('spoticar')

# Fonction pour lancer une collecte de données
def start_scraping():
    subprocess.run(["scrapy", "crawl", "SpoticarSpider"])

# Fonction pour télécharger les données
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="spoticar.csv">Télécharger les données</a>'

# Fonction pour récupérer toutes les voitures
def get_all_voitures():
    return voitures

# Fonction pour filtrer les voitures en fonction de la lettre (avec "Tout" par défaut)
def get_voitures_by_letter(voitures, letter="Tout"):
    if letter == "Tout":
        return voitures
    else:
        return [voiture for voiture in voitures if voiture[0].startswith(letter)]
    
# Fonction pour filtrer les voitures en fonction du prix
def get_voitures_by_price(voitures, prix_range):
    min_prix, max_prix = prix_range
    return [voiture for voiture in voitures if min_prix <= int(voiture[2].replace(' ', '').replace('€', '')) <= max_prix]

