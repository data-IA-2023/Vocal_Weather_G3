from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

def extract_entities(text):
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    cities = []
    dates = []

    for entity in blob.noun_phrases:
        if 'ville' in entity:
            cities.append(entity)
        elif 'date' in entity:
            dates.append(entity)

    return cities, dates

text = "Je vais à Paris demain."
cities, dates = extract_entities(text)
print("Villes:", cities)
print("Dates:", dates)
