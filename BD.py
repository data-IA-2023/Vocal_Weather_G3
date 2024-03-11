from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la connexion à la base de données Azure SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=serveurbdg7.database.windows.net;DATABASE=vocal_weather;UID=mohammed@serveurbdg7;PWD=password@123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Définition du modèle de la table dans la base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Route pour tester la connexion à la base de données
@app.route('/')
def index():
    try:
        db.session.query(User).first()
        return 'Connexion à la base de données réussie!'
    except Exception as e:
        return f'Erreur lors de la connexion à la base de données: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
