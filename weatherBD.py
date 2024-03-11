import pyodbc
from dotenv import load_dotenv
import os

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