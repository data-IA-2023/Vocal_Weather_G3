from datetime import datetime, timedelta
import re
import dateparser
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from fuzzywuzzy import fuzz
import datefinder

def camembertNlp(phrase=""):
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    doc=nlp(phrase)
    
    return doc


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
    elif expression_temporelle == "la semaine prochaine":
        # Pour obtenir le début de la semaine prochaine, on soustrait les jours déjà passés
        jours_restants_semaine = 7 - aujourdhui.weekday()
        date = aujourdhui + timedelta(days=jours_restants_semaine)
    elif expression_temporelle == "la semaine d'après":
        # Pour obtenir le début de la semaine d'après, on ajoute 7 jours à la fin de la semaine actuelle
        jours_restants_semaine = 7 - aujourdhui.weekday()
        date = aujourdhui + timedelta(days=7 + jours_restants_semaine)
    else:
        return None
    # Formater la date en YYYY-MM-DD
    date_formattee = date.strftime("%Y-%m-%d")
    return date_formattee
    
 # Fonction pour trouver la meilleure correspondance pour une expression temporelle incorrecte
def trouver_correspondance(expression_temporelle):
    expressions_temporelles = ["après-demain", "demain", "aujourd'hui", "hier", "avant-hier", "la semaine prochaine", "la semaine d'après"]
    max_score = -1
    meilleure_correspondance = None
    for temporelle in expressions_temporelles:
        score = fuzz.ratio(expression_temporelle, temporelle)
        if score > max_score:
            max_score = score
            meilleure_correspondance = temporelle
    return meilleure_correspondance

def formatDate(phrase):
        # dates_trouvees = datefinder.find_dates(phrase.lower())
        date=None
        dates_trouvees = dateparser.parse(phrase.lower(), languages=["fr"])
        if dates_trouvees:
            date = dates_trouvees.strftime("%Y-%m-%d")
        return date
        
def NLP(phrase=""):
    ville = []
    date = []
    doc = camembertNlp(phrase=phrase)
    for ent in doc:
        if ent['entity_group'] == 'LOC':
            ville.append(ent['word'])
            
        if ent['entity_group'] == 'DATE':
            word = ent['word']
            d = formatDate(word)
            if not d:
                d = trouver_correspondance(word)
                d = convertir_date(d)
            date.append(d)
    return {'ville':ville, 'date':date}
 

if __name__== "__main__":
    phrase_test = "Je veux la météo à tours demain"
    resultat= NLP(phrase_test)    
    print('ville =', resultat['ville'])    
    print('date =', resultat['date'])
