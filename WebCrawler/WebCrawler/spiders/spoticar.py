import scrapy
from scrapy import Request
from WebCrawler.items import SpoticarListItem
from WebCrawler.pipelines import *


class SpoticarSpider(scrapy.Spider):
    name = "spoticar"
    allowed_domains = ["www.spoticar.fr"]
    start_urls = ["https://www.spoticar.fr/voitures-occasion?page=%s" % page for page in range(1, 1000)]
    database = DataBase('spoticar')

    # Create table
    try:
      database.create_table('spoticar',
        modele = db.String,
        version = db.String,
        prix = db.String,
        nbr_km = db.String,
        moteur = db.String,
        annee = db.String,
        boite = db.String,
        lieu = db.String,
        photo = db.String,
      )
    except:
      pass

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_spoticar)

    def parse_spoticar(self, response):
        # Liste des voiture en vente
        list_voitures = response.css('div.reskin-product-card')

        for voiture in list_voitures:
            item = SpoticarListItem()

            # Modèle de la voiture
            try:
              item['modele'] = voiture.css('h3 span.title::text').get().strip()
            except:
              item['modele'] = 'None'

            # Version du modèle
            try:
              item['version'] = voiture.css('h3 span.sub-title::text').get().strip()
            except:
              item['version'] = 'None'

            # Prix de la voiture
            try:
              item['prix'] = voiture.css('p.price span::text').get().strip()
            except:
              item['prix'] = 'None'

            # Nombre de kilomètres
            try:
              item['nbr_km'] = voiture.css('ul.tags li:nth-child(1)::text').get().strip()
            except:
              item['nbr_km'] = 'None'

            # Moteur
            try:
              item['moteur'] = voiture.css('ul.tags li:nth-child(2)::text').get().strip()
            except:
              item['moteur'] = 'None'

            # Année
            try:
              item['annee'] = voiture.css('ul.tags li:nth-child(3)::text').get().strip()
            except:
              item['annee'] = 'None'

            # Boite
            try:
              item['boite'] = voiture.css('ul.tags li:nth-child(4)::text').get().strip()
            except:
              item['boite'] = 'None'

            # Lieu
            try:
              item['lieu'] = voiture.css('p.address span.localisation::text').get().strip()
            except:
              item['lieu'] = 'None'

            # Photo
            try:
              item['photo'] = voiture.css('div.ratio-container img::attr(data-src)').get()
            except:
              item['photo'] = 'None'

            self.database.add_row('spoticar', 
                modele = item['modele'],
                version = item['version'],
                prix = item['prix'],
                nbr_km = item['nbr_km'],
                moteur = item['moteur'],
                annee = item['annee'],
                boite = item['boite'],
                lieu = item['lieu'],
                photo = item['photo'],
            )

            yield item
