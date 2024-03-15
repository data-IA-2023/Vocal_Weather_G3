"""
Service for geocoding :
=====================

This module can be processed as following :
- `city` as a string is passed from the user input.
- The Nominatim geocoder (from Open Street Map) is invoked.
- The `user_agent` should be declared for OSM' monitoring purpose. `user_agent` is the name of your service.


Ressources :
- Geopy : https://github.com/geopy/geopy
- Open Street Map : https://www.openstreetmap.fr/
"""

from geopy.geocoders import Nominatim
from sys import argv

def city_to_coordinates(city):
    
    # Define the name of your app (for external service monitoring)
    geolocator = Nominatim(user_agent="Chatmeteo")
    
    # Send the user' city to geocode service
    location = geolocator.geocode(city)
    
    # Extract desired data : coordinates
    lat = location.latitude
    lon = location.longitude
    
    # Return
    print(f'Latitude, Longitude : {lat, lon}')
    return({'lat': lat,
            'lon' : lon})

# Test
# city_to_coordinates(city='Tours')

# Execution du script seulement s'il est appelé directement dans le terminal, sinon chargement uniquement sans exécution
if __name__ == "__main__":

    city_to_coordinates(argv[1])