import pyodbc

SERVER = 'serveurbdg7.database.windows.net,1433'
DATABASE = 'vocal_weather'
USERNAME = 'mohammed'
PASSWORD = 'password@123'

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
