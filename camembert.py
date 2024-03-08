import datetime
from datetime import timedelta
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from fuzzywuzzy import fuzz


def camembertNlp(phrase=""):
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    doc=nlp(phrase)
    
    return doc


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
    
    
phrase = " la méteo à Joué les Tours apres demain"

print(camembertNlp(phrase=phrase))