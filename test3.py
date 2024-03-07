import spacy
from datetime import datetime

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

# Exemple de phrase
phrase = "Quel temps fait-il à New York à la date 22/01/2024 ?"

# Analyser la phrase avec spaCy
doc = nlp(phrase)

# Initialiser la variable pour stocker la date
date = None

# Parcourir les entités dans le document
for ent in doc.ents:
    if ent.label_ == "DATE":
        # Si l'entité est de type DATE, essayez de la convertir en date
        try:
            date = datetime.strptime(ent.text, "%d %B %Y")
            break  # Sortir de la boucle dès que la première date est trouvée
        except ValueError:
            pass  # Ignorer les entités qui ne peuvent pas être converties en date

# Si une date est trouvée, formatez-la au format souhaité
if date:
    formatted_date = date.strftime("%Y-%m-%d")
    print("Date détectée:", formatted_date)
else:
    print("Aucune date détectée.")
