import json
from flask import Flask, render_template, request, abort, Response
import urllib
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from voice import recognize_from_microphone
from camembert import NLP
from geocoding import city_to_coordinates
from apimeteo import apimeteo
from weatherBD import connectBd, inserer_donnees_surveillance

load_dotenv('.env')
conn=connectBd()
    
app = Flask(__name__)


@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('ville')
    date_str = request.args.get('date')
    
    inserer_donnees_surveillance(conn,'forecast', 'resultat', 200)
    
    if city is None or date_str is None:
        abort(400, 'Missing argument city or date')
        
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        abort(400, 'Invalid date format. Please use YYYY-MM-DD')
    
    data = {}
    location = city_to_coordinates(city)
    if location is None:
        abort(400, 'Invalid city')
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    date_demain_str = date_str #temp pour le test
    
    # date_demain = date_obj + timedelta(days=1)
    # date_demain_str = date_demain.strftime("%Y-%m-%d")

    df=apimeteo(lat=location['lat'],lon=location['lon'],start_date=date_str,end_date=date_demain_str)
    table = df.to_html(index=False)
    titre= f'La météo à {city} le {date_str} est:'

    return render_template('index2.html', titre=titre, table=table)




@app.route('/speech-to-text', methods=['post'])
def speechToText():
    result= recognize_from_microphone()
    return render_template('index.html', result = result)

@app.route('/decode', methods=['GET'])
def decode():
    phrase = request.args.get('speech_text')
    data= NLP(phrase=phrase)
    ville = data.get('ville', [''])[0]
    date = data.get('date', [''])[0]
    return render_template('index.html', ville = ville, date= date)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)