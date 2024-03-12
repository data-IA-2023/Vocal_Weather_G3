import re
import spacy
import requests
from datetime import datetime, timedelta
import dateparser
from dotenv import load_dotenv
import os
import datefinder

load_dotenv('.env')
# Charger le modèle de langue français de SpaCy
nlp = spacy.load("fr_core_news_lg")

def extraire_ville_et_date(phrase):
    doc = nlp(phrase)
    ville = None
    date = None

    for ent in doc.ents:
        # print(ent.text, ent.label_)
        if ent.label_ in ["LOC", "GPE"]:
            ville = ent.text
        elif ent.label_ == "DATE":
            date = ent.text.lower().strftime("%Y-%m-%d")

    
    for token in doc:
        # print(token.text, token.ent_type_)
        if token.ent_type_ == "DATE":
            date = token.text.lower().strftime("%Y-%m-%d")
        elif token.text.lower() == "demain":
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif token.text.lower() == "aujourd'hui":
            date = datetime.now().strftime("%Y-%m-%d")
        elif token.text.lower() == "après-demain":
            date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        elif (token.text.lower() == "avant-hier"):
            date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        elif token.text.lower() == "hier":
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    
    if not date:
        dates_trouvees = datefinder.find_dates(phrase.lower())
        premiere_date = next(dates_trouvees, None)
        if premiere_date:
            date = premiere_date.strftime("%Y-%m-%d")

    if not date:
        date = recherchedate(phrase)
        if date:
            date = date.strftime("%Y-%m-%d")

    return ville, date

def recherchedate(sentence):

    # Expression régulière pour extraire la date
    date_pattern = r"\b(\d{1,2} (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) \d{4})\b"

    # Recherche de la date dans la phrase
    match = re.search(date_pattern, sentence)

    if match:
        date_str = match.group(1)
        parsed_date = dateparser.parse(date_str, languages=["fr"])
        if parsed_date:
            date = parsed_date.strftime("%Y-%m-%d")
            return date




    
def obtenir_meteo(ville, date):
    # Votre clé d'API OpenWeatherMap (à remplacer par votre propre clé)
    api_key = os.environ['METEOKEY']
    
    # Formatage de la date pour la requête API
    formatted_date = date
    
    # Requête à l'API OpenWeatherMap pour obtenir les informations météorologiques
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&date={formatted_date}&appid={api_key}"
    response = requests.get(url)
    
    # Vérification de la réponse de l'API
    if response.status_code == 200:
        meteo_data = response.json()
        return meteo_data
    else:
        return {"error": "Impossible d'obtenir les données météorologiques"}


def main(phrase):
    ville, date = extraire_ville_et_date(phrase)
    print(ville, 'est', date)
    if ville and date:
        
        meteo = obtenir_meteo(ville, date)
        print("Informations météorologiques :", meteo)
        return meteo
    else:
        print("Impossible de détecter la ville ou la date dans la phrase.")
        return {"error": "Ville ou date manquante"}

# Exemple d'utilisation
if __name__== "__main__":
    phrase_test = "Quel temps fait-il à New york le 10 mars ?"
    main(phrase_test)
