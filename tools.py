import requests
import math

def get_ll_spn(obj):
    coords = obj["Point"]["pos"]
    lowerx, lowery = obj["boundedBy"]["Envelope"]["lowerCorner"].split()
    upperx, uppery = obj["boundedBy"]["Envelope"]["upperCorner"].split()
    deltax = (float(upperx) - float(lowerx)) / 2
    deltay = (float(uppery) - float(lowery)) / 2
    return (','.join(coords.split()), (deltax,deltay))

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
            return get_ll_spn(toponym)
        else:
            return 'err1'    
    except Exception:
        return 'err2'   

def static_mapper(data, points = []):
    if data != 'err1' or 'err2':
        ll = data[0]
        spn = data[1]
        if points != []:
            points = '~' + '~'.join(points)
        else: points = ''
        static_api_address = "http://static-maps.yandex.ru/1.x/?"
        static_api_params = "ll={}&spn={},{}&pt={}&l=map".format(ll, spn[0], spn[1], ll + points)
        address = static_api_address + static_api_params
        print(address)
        return (address, ll)
    return ll

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a[0], a[1]
    b_lon, b_lat = b[0], b[1]

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)
    return distance

def convert_to_degrees(meters):
    one_meter = 1 / 111000
    return str(meters * one_meter)

def get_organisation(coords, spn):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "3c4a592e-c4c0-4949-85d1-97291c87825c"
    
    search_params = {
        "apikey": api_key,
        "lang": "ru_RU",
        "ll": coords,
        "type": "biz"
    }
    
    response = requests.get(search_api_server, params=search_params)
    if not response:
        return "err4"
    json_response = response.json()
    if len(json_response["features"]) != 0:
        points = []
        for i in json_response["features"]:
            if lonlat_distance(i["geometry"]["coordinates"], list(map(float, coords.split(',')))) <= int(spn):
                points.append(','.join(map(str, i["geometry"]["coordinates"])))
        return points
    return "err5"