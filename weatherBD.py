from datetime import datetime
import pyodbc
from dotenv import load_dotenv
import os


def connectBd():
    
    load_dotenv('.env')
    SERVER = os.environ['SERVER']
    DATABASE = os.environ['DATABASE']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString)
    return conn


def inserer_donnees_surveillance(conn, fonction, resultat, erreur):
    # try:
        cursor = conn.cursor()
        query = "INSERT INTO vocal_weather.dbo.table_surveillance (date_evenement, fonction, resultat, erreur) VALUES (?, ?, ?, ?)"
        data = (datetime.now(), fonction, resultat, erreur)
        cursor.execute(query, data)
        conn.commit()
        print("Données de surveillance insérées avec succès.")
    # except Exception  as e:
    #     print(f"Erreur lors de l'insertion des données de surveillance: {e}")
        


def test():
    
    load_dotenv('.env')

    SERVER = os.environ['SERVER']
    DATABASE = os.environ['DATABASE']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString) 

    SQL_QUERY = """
    SELECT *
    FROM vocal_weather.dbo.monitoring
    ;
    """
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)

    records = cursor.fetchall()
    for r in records:
        print(f"LIGNE: {r}")

    cursor.close()
    conn.close()