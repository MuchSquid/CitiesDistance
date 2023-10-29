from flask import Flask, render_template, request, jsonify
import requests
import math
import csv

app = Flask(__name__)

BASE_URL = "https://nominatim.openstreetmap.org/search?q={}&format=json"


class CoordinatesFactory:
    def get_coords_method(self, method_type):
        if method_type == "api":
            return APICoordinates()
        elif method_type == "csv":
            return CSVCoordinates()
        elif method_type == "mock":
            return MockCoordinates()
        else:
            raise ValueError("Invalid method type")


class APICoordinates:
    def get_coords(self, city):
        response = requests.get(BASE_URL.format(city))
        if response.status_code != 200:
            return None, None

        data = response.json()
        if not data:
            return None, None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        return lat, lon


class CSVCoordinates:
    def get_coords(self, city):
        with open('worldcities.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Verificamos si la ciudad coincide (ciudad se encuentra en la columna 0)
                if row[0].lower() == city.lower():
                    # Latitud está en la columna 2 y Longitud en la columna 3
                    return float(row[2]), float(row[3])
        return None, None


class MockCoordinates:
    def get_coords(self, city):
        # This is just for demonstration purposes, it will return fixed coordinates
        return 40.730610, -73.935242  # New York coordinates for all cities


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    if None in [lat1, lon1, lat2, lat2]:
        return 0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular_distancia', methods=['POST'])
def calcular_distancia():
    ciudad1 = request.form.get('ciudad1')
    ciudad2 = request.form.get('ciudad2')
    method_type = request.form.get('method_type')


    factory = CoordinatesFactory()
    method = factory.get_coords_method(method_type)

    lat1, lon1 = method.get_coords(ciudad1)
    lat2, lon2 = method.get_coords(ciudad2)

    if lat1 is None or lat2 is None:
        return render_template('error.html'), 400 
    
    distancia = haversine(lat1, lon1, lat2, lon2)


    if method_type == 'csv':
        return render_template('resultado_csv.html', ciudad1=ciudad1, ciudad2=ciudad2, distancia=distancia)
    else:
        return render_template('resultado.html', ciudad1=ciudad1, ciudad2=ciudad2, distancia=distancia)


if __name__ == '__main__':
    app.run(debug=True)
