# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpoticarListItem(scrapy.Item):
    modele = scrapy.Field()
    version = scrapy.Field()
    prix = scrapy.Field()
    nbr_km = scrapy.Field()
    moteur = scrapy.Field()
    annee = scrapy.Field()
    boite = scrapy.Field()
    lieu = scrapy.Field()
    photo = scrapy.Field()