import re
import dateparser
import textacy
import datetime

def extract_entities(text):
    # Charger le modèle linguistique en français
    fr = textacy.load_spacy_lang("fr_core_news_lg")

    # Initialiser les variables
    ville = None
    date = None

    # Traitement du texte
    doc = textacy.make_spacy_doc(text, lang=fr)

    # Extraction des entités nommées
    for ent in doc.ents:
        if ent.label_ == "LOC":
            ville = ent.text
        elif ent.label_ == "DATE":
            date = ent.text
    if not date:
        date = datefinder(phrase)

    return ville, date

def datefinder(sentence):

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

# Exemple de phrase
phrase = "Quel temps fait-il à Paris demain ?"

# Extraction des entités
ville, date = extract_entities(phrase)

# Affichage des résultats
print("Ville:", ville)
print("Date:", date)