from math import sqrt, pow
import random

class City():
    x: int
    y: int
    name: str
    
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.x = x
        self.y = y
    
    @staticmethod
    def calculate_distance(city1: 'City', city2: 'City') -> float:
        return sqrt(pow(city1.x - city2.x, 2) + pow(city1.y - city2.y, 2))
    
    @staticmethod
    def generate_random_cities(cities_count: int, max_x: int = 30, max_y: int = 30) -> list['City']:
        cities = []
        for i in range(cities_count):
            cities.append(City(f"City {i+1}", random.randint(0, max_x), random.randint(0, max_y)))
        return cities
    
    def __str__(self):
        return f"{self.name} ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()