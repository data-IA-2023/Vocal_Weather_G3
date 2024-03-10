import json
from flask import Flask, render_template, request, abort, Response
import urllib
from dotenv import load_dotenv
import os
from datetime import datetime

from voice import recognize_from_microphone
from camembert import NLP



load_dotenv('.env')
app = Flask(__name__)


@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('ville')
    date_str = request.args.get('date')
    
    if city is None or date_str is None:
        abort(400, 'Missing argument city or date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        abort(400, 'Invalid date format. Please use YYYY-MM-DD')
    
    data = {}
    data['q'] = city
    data['appid'] = os.environ['METEOKEY']
    data['units'] = 'metric'
    data['dt'] = int(date.timestamp())  # Convert date to Unix timestamp
    
    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    full_url = url + '?' + url_values
    response = urllib.request.urlopen(full_url)
    
    resp = Response(response)
    resp.status_code = 200
    titre= f'La météo à {city} le {date_str} est'
    return render_template('index.html', titre=titre, data=json.loads(response.read().decode('utf8')))

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