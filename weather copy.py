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
from surveillance import connectBd, inserer_donnees_surveillance


    
app = Flask(__name__)

load_dotenv('.env')
conn=connectBd()


@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('ville')
    date_str = request.args.get('date')
    

    if city is None or date_str is None:
        inserer_donnees_surveillance(conn,'forecast_Arg', 'Missing argument city or date', 400)
        abort(400, 'Missing argument city or date')
    else:
        inserer_donnees_surveillance(conn,'forecast_Arg', f'city : {city} and date : {date_str}', 200)
    

    try:
        location = city_to_coordinates(city)
    except Exception as e:
        inserer_donnees_surveillance(conn,'geocoding', f'Geacoding API erreur :{city}', e)
        abort(400, 'Geacoding API erreur')
    
 
    if location is None:
        inserer_donnees_surveillance(conn,'geocoding', f'Invalid city :{city}', 400)
        abort(400, 'Invalid city')
    else:
        inserer_donnees_surveillance(conn,'geocoding', f"lat : {location['lat']} and lon : {location['lon']}", 200)
    
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    date_demain_str = date_str #temp pour le test
    
    # date_demain = date_obj + timedelta(days=1)
    # date_demain_str = date_demain.strftime("%Y-%m-%d")
    
    try:
        df=apimeteo(lat=location['lat'],lon=location['lon'],start_date=date_str,end_date=date_demain_str)
        table = df.to_html(index=False)
    except Exception as e:
        inserer_donnees_surveillance(conn,'apimeteo', f"Erreur in apiMeteo for this location lat : {location['lat']} and lon : {location['lon']}", 400)
    else:
        inserer_donnees_surveillance(conn,'apimeteo', f"No problemo : {location['lat']} and lon : {location['lon']}", 200)    
            
    titre= f'La météo à {city} le {date_str} est:'

    return render_template('index2.html', titre=titre, table=table)




@app.route('/speech-to-text', methods=['post'])
def speechToText():
    result= recognize_from_microphone()
    
    if result is None :
        inserer_donnees_surveillance(conn,'speechToText', 'No speech could be recognized', 400)
        abort(400, 'No speech could be recognized')
    else:
        inserer_donnees_surveillance(conn,'speechToText', result, 200)
    
    return render_template('index.html', result = result)



@app.route('/decode', methods=['GET'])
def decode():
    
    try:
        phrase = request.args.get('speech_text')
        data= NLP(phrase=phrase)
        # ville = data.get('ville', [''])[0]
        # date = data.get('date', [''])[0]
        ville = data['ville'][0]
        date = data['date'][0]
    except Exception as e:
        inserer_donnees_surveillance(conn,'NLP', f'NLP api can not process this :{phrase}', e)
        abort(400, 'Missing city or date')
        
    if ville is None or date is None:
        inserer_donnees_surveillance(conn,'NLP', f'Missing city or date in :{phrase}', 400)
        abort(400, 'Missing city or date')
    else:
        inserer_donnees_surveillance(conn,'NLP', f'city : {ville} and date : {date}', 200)
    
    return render_template('index.html', ville = ville, date= date)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
