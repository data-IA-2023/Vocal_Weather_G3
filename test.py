from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from dateutil.parser import parse

# Initialisation de SparkSession
spark = SparkSession.builder \
    .appName("Spark NLP") \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.1.0") \
    .getOrCreate()

# Phrase d'exemple
phrase = "La réunion aura lieu à Paris le 10 mars 2024."

# Création d'un DataFrame Spark avec la phrase
data = spark.createDataFrame([(phrase,)], ["text"])

# Chargement du modèle NER de Spark NLP
documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
ner_model = 'ner_dl'
ner_pipeline = PretrainedPipeline(ner_model, lang="fr")

# Application du modèle NER pour extraire les entités nommées
result = ner_pipeline.transform(data)

# Extraction des entités nommées (ici, on récupère les entités de type "LOC" pour la ville et "DATE" pour la date)
entities = result.selectExpr("explode(ner) as entities") \
                 .select("entities.result", "entities.metadata") \
                 .where("metadata['entity'] in ('LOC', 'DATE')")

# Filtrage des entités pour récupérer la ville et la date
ville = entities.filter("metadata['entity'] == 'LOC'").select("result").collect()[0][0]
date = entities.filter("metadata['entity'] == 'DATE'").select("result").collect()[0][0]

print("Ville:", ville)
print("Date:", date)