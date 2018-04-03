import requests

def get_ll(obj):
    coords = obj["Point"]["pos"]
    lowerx, lowery = obj["boundedBy"]["Envelope"]["lowerCorner"].split()
    upperx, uppery = obj["boundedBy"]["Envelope"]["upperCorner"].split()
    deltax = (float(upperx) - float(lowerx)) / 2
    deltay = (float(uppery) - float(lowery)) / 2
    return ','.join(coords.split())

def geocoder(text):
    try:
        geocoder_url = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_url, params={
            "format": "json",
            "geocode": text
        })
        toponym = response.json()
        if len(toponym["response"]["GeoObjectCollection"]["featureMember"]) != 0:
            toponym = toponym["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            return get_ll(toponym)
        else:
            return 'err1'    
    except Exception:
        return 'err2'   

def static_mapper(data):
    ll = data
    if ll != 'err1' or 'err2':
        spn = "0.02"
        static_api_address = "http://static-maps.yandex.ru/1.x/?"
        static_api_params = "ll={}&spn={}&pt={}&l=map".format(ll, spn, ll)
        address = static_api_address + static_api_params
        return address
    else:
        return ll