import spacy
import requests
from datetime import datetime, timedelta
import dateparser
from dotenv import load_dotenv
import os

load_dotenv('.env')
# Charger le modèle de langue français de SpaCy
nlp = spacy.load("fr_core_news_sm")

def extraire_ville_et_date(phrase):
    # Analyser la phrase avec SpaCy
    doc = nlp(phrase)
    
    ville = None
    date = None
    
    # Parcourir les tokens dans le document
    for token in doc:
        # Vérifier si le token est une ville (ex: Paris, New York, etc.)
        if token.ent_type_ in ["LOC", "GPE"]:
            ville = token.text
        
        # Vérifier si le token est une date spéciale
        if token.text.lower() == "demain":
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")   
        elif token.text.lower() == "aujourd'hui":
            date = datetime.now().strftime("%Y-%m-%d")
        elif token.text.lower() == "hier":
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif token.pos_ == "NOUN":
            # Utiliser dateparser pour analyser les dates sous forme de noms
            date = dateparser.parse(token.text, languages=["fr"])
            if date:
                date = date.strftime("%Y-%m-%d")
        elif token.ent_type_ == "DATE":
            # Utiliser dateparser pour analyser les autres dates
            date = token.text.lower()  # ou dateparser.parse(token.text, languages=["fr"])
    
    return ville, date

    
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
    if ville and date:
        meteo = obtenir_meteo(ville, date)
        print("Informations météorologiques :", meteo)
        return meteo
    else:
        print("Impossible de détecter la ville ou la date dans la phrase.")
        return {"error": "Ville ou date manquante"}

# Exemple d'utilisation
phrase_test = "Quel temps fait-il à Paris samedi prochain?"
main(phrase_test)
