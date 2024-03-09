import spacy
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

# Fonction pour convertir les expressions temporelles en dates
def convertir_date(expression_temporelle):
    # Obtenir la date actuelle
    aujourdhui = datetime.today()
    # Obtenir les dates relatives en fonction de l'expression temporelle
    if expression_temporelle == "après-demain":
        date = aujourdhui + timedelta(days=2)
    elif expression_temporelle == "demain":
        date = aujourdhui + timedelta(days=1)
    elif expression_temporelle == "aujourd'hui":
        date = aujourdhui
    elif expression_temporelle == "hier":
        date = aujourdhui - timedelta(days=1)
    elif expression_temporelle == "avant-hier":
        date = aujourdhui - timedelta(days=2)
    else:
        return None
    # Formater la date en YYYY-MM-DD
    date_formattee = date.strftime("%Y-%m-%d")
    return date_formattee

# Fonction pour trouver la meilleure correspondance pour une expression temporelle incorrecte
def trouver_correspondance(expression_temporelle):
    expressions_temporelles = ["après-demain", "demain", "aujourd'hui", "hier", "avant-hier"]
    max_score = -1
    meilleure_correspondance = None
    for temporelle in expressions_temporelles:
        score = fuzz.ratio(expression_temporelle, temporelle)
        if score > max_score:
            max_score = score
            meilleure_correspondance = temporelle
    return meilleure_correspondance

# Exemple d'utilisation
texte = "Demian, c'est demin, hiers, avan-hier, et après demain c'est après-démain."
doc = nlp(texte)

# Parcourir les jetons (tokens) pour trouver les expressions temporelles
for token in doc:
    expression_temporelle = token.text.lower()
    correspondance = trouver_correspondance(expression_temporelle)
    if correspondance:
        date_formattee = convertir_date(correspondance)
        if date_formattee:
            print(f"{expression_temporelle}: {date_formattee}")
