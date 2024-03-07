from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


def camembertNlp(phrase=""):
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    doc=nlp(phrase)
    return doc
    
    
phrase = " la méteo à Joué les Tours demain"

print(camembertNlp(phrase=phrase))