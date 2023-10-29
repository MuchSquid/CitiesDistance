"""
Dada la aplicación que realizaron para cálculo de distancia:
Elaborar e implementar pruebas unitarias.
Elaborar casos de prueba manual con el formato Precondition, Test Steps, Test Data, Expected
Result.
• Mostrar que se puedan ejecutar en su aplicación.
• Considerar:
Caso de éxito.
2 Casos extremos: una de las ciudades no exista y entregar la misma ciudad dos veces

"""
import unittest
from app import *

class MyTestCase(unittest.TestCase):
    def test_cal_distance(self):
        ciudad1 = "Lima, Peru"
        ciudad2 = "Bogota, Colombia"
        method_type = "api"

        factory = CoordinatesFactory()
        method = factory.get_coords_method(method_type)

        lat1, lon1 = method.get_coords(ciudad1)
        lat2, lon2 = method.get_coords(ciudad2)

        distancia = haversine(lat1, lon1, lat2, lon2)

        self.assertEqual(round(distancia, 2), 1887.09)

 
    def test_city_does_not_exist(self):
        ciudad1 = "CiudadInexistente1"
        ciudad2 = "Lima, Peru"
        method_type = "api"

        factory = CoordinatesFactory()
        method = factory.get_coords_method(method_type)

        lat1, lon1 = method.get_coords(ciudad1)
        lat2, lon2 = method.get_coords(ciudad2)

        # Verifica que las coordenadas sean None para la ciudad1:
        self.assertIsNone(lat1)
        self.assertIsNone(lon1)

        # Verifica que las coordenadas sean distintas de None para la ciudad2:
        self.assertIsNotNone(lat2)
        self.assertIsNotNone(lon2)

    def test_both_cities_do_not_exist(self):
        ciudad1 = "CiudadInexistente1"
        ciudad2 = "CiudadInexistente2"
        method_type = "api"

        factory = CoordinatesFactory()
        method = factory.get_coords_method(method_type)

        lat1, lon1 = method.get_coords(ciudad1)
        lat2, lon2 = method.get_coords(ciudad2)

        # Verifica que las coordenadas sean None para ambas ciudades:
        self.assertIsNone(lat1)
        self.assertIsNone(lon1)
        self.assertIsNone(lat2)
        self.assertIsNone(lon2)


    def test_same_city(self):
        ciudad1 = "Lima, Peru"
        ciudad2 = "Lima, Peru"
        method_type = "mock"

        factory = CoordinatesFactory()
        method = factory.get_coords_method(method_type)

        lat1, lon1 = method.get_coords(ciudad1)
        lat2, lon2 = method.get_coords(ciudad2)

        distancia = haversine(lat1, lon1, lat2, lon2)

        self.assertEqual(distancia, 0)

if __name__ == "__main__":
    unittest.main()