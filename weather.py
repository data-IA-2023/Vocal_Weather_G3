import json
from flask import Flask, render_template, request, abort, Response
import urllib

app = Flask(__name__)


@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city is None:
        abort(400, 'Missing argument city')
    
    data = {}
    data['q'] = city
    data['appid'] = 'bb6143fe4e36b6f74f55e36b8e49f14a'
    data['units'] = 'metric'
    
    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    full_url = url + '?' + url_values
    data = urllib.request.urlopen(full_url)
    
    resp = Response(data)
    resp.status_code = 200
    return render_template('index.html', title='Weather App', data=json.loads(data.read().decode('utf8')))