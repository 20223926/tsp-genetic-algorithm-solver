from city import City
import random
import matplotlib.pyplot as plt

class TSP():
    cities: list[City]
    population: list[list[City]]

    def __init__(self, cities_list: list[City], population_size: int) -> None:
        self.cities = cities_list
        self.population = [random.sample(self.cities, len(self.cities)) for _ in range(population_size)]
    
    def calculate_total_distance(self, genome: list[City]) -> float:
        total_distance = 0
        for i in range(len(genome)):
            current_city = genome[i]
            next_city = genome[(i + 1) % len(genome)] # Loop back to the first city after visiting the last one
            total_distance += City.calculate_distance(current_city, next_city)
        return total_distance

    def get_fitnesses(self, population: list[list[City]]) -> list[float]:
        # Convert distances to fitness values (higher is better)
        total_distances = [self.calculate_total_distance(genome) for genome in population]
        max_distance = max(total_distances)
        return [max_distance - distance for distance in total_distances]
    
    def order_crossover(self, parent1: list[City], parent2: list[City]) -> tuple[list[City], list[City]]:
        # OX: Preserves relative order by selecting segment from one parent and maintaining order from the other
        size = len(parent1)
        point1, point2 = sorted(random.sample(range(size), 2))

        def create_ox_child(p1: list[City], p2: list[City]) -> list[City]:
            child = [None] * size
            child[point1:point2+1] = p1[point1:point2+1]

            p2_index = 0
            for i in range(size):
                if child[i] is None:
                    while p2[p2_index] in child:
                        p2_index += 1
                    child[i] = p2[p2_index]
            return child
        
        child1 = create_ox_child(parent1, parent2)
        child2 = create_ox_child(parent2, parent1)
        return child1, child2
    
    def order_one_crossover(self, parent1: list[City], parent2: list[City]) -> tuple[list[City], list[City]]:
        # OX1: Single point crossover version of OX
        crossover_point = random.randint(0, len(parent1)-1)
        child1 = list(parent1[:crossover_point])
        child1 += [city for city in parent2 if city not in child1]
        child2 = list(parent2[:crossover_point])
        child2 += [city for city in parent1 if city not in child2]
        return child1, child2
    
    def partially_mapped_crossover(self, parent1: list[City], parent2: list[City]) -> tuple[list[City], list[City]]:
        # PMX: Creates mappings between corresponding cities in the selected segment
        size = len(parent1)
        point1, point2 = sorted(random.sample(range(size), 2))

        def create_pmx_child(p1: list[City], p2: list[City]) -> list[City]:
            child = [None] * size
            child[point1:point2+1] = p1[point1:point2+1]
            mapping = {p1[i]: p2[i] for i in range(point1, point2+1)}

            for i in range(size):
                if i < point1 or i > point2:
                    p2_current = p2[i]
                    while p2_current in mapping:
                        p2_current = mapping[p2_current]
                    child[i] = p2_current
            return child
        
        child1 = create_pmx_child(parent1, parent2)
        child2 = create_pmx_child(parent2, parent1)
        return child1, child2
    
    def mutation(self, genome: list[City], mutation_prob: float) -> list[City]:
        if random.random() < mutation_prob:
            i1 = round(random.uniform(0, len(genome) - 1))
            i2 = round(random.uniform(0, len(genome) - 1))
            genome[i1], genome[i2] = genome[i2], genome[i1]
        return genome
    
    def select_parents_roulette_wheel(self) -> tuple[list[City], list[City]]:
        if len(self.population) < 2:
            raise ValueError("Population size must be at least 2 to select parents.")
        
        fitnesses = self.get_fitnesses(self.population)
        # Roulette wheel works with fitness probabilities, so we need to normalize them
        total_fitness = sum(fitnesses)
        fitness_probabilities = [fitness / total_fitness for fitness in fitnesses]

        parent1 = random.choices(self.population, weights=fitness_probabilities, k=1)[0]
        parent2 = parent1
        while parent2 == parent1:
            parent2 = random.choices(self.population, weights=fitness_probabilities, k=1)[0]
        return parent1, parent2
    
    def select_parents_tournament(self, tournament_size: int) -> tuple[list[City], list[City]]:
        if len(self.population) < 2:
            raise ValueError("Population size must be at least 2 to select parents.")
        if (len(self.population) < tournament_size):
            raise ValueError("Tournament size must be less than or equal to population size.")
        
        def select_tournament_winner():
            candidates = random.sample(self.population, tournament_size)
            fitnesses = self.get_fitnesses(candidates)
            candidates_with_fitness = [(candidate, fitness) for candidate, fitness in zip(candidates, fitnesses)]
            candidates_with_fitness.sort(key=lambda x: x[1], reverse=True)
            return candidates_with_fitness[0][0]
        
        parent1 = select_tournament_winner()
        parent2 = select_tournament_winner()
        return parent1, parent2

    def run(self, generations_limit: int, mutation_prob: float, elite_count: int, selection_method: int = 1, tournament_size: int = 3, crossover_method: int = 3) -> None:
        best_distances = []
        plt.ion()
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        for _ in range(generations_limit):
            # Elitism: preserve best solutions
            sorted_population = sorted(self.population, key=self.calculate_total_distance)
            elites = sorted_population[:elite_count]
            
            new_population = []
            for _ in range((len(self.population) - elite_count) // 2):
                if selection_method == 1:
                    parent1, parent2 = self.select_parents_tournament(tournament_size)
                else:
                    parent1, parent2 = self.select_parents_roulette_wheel()
                
                if crossover_method == 1:
                    child1, child2 = self.order_crossover(parent1, parent2)
                elif crossover_method == 2:
                    child1, child2 = self.order_one_crossover(parent1, parent2)
                else:
                    child1, child2 = self.partially_mapped_crossover(parent1, parent2)
                
                new_population.append(self.mutation(child1, mutation_prob))
                new_population.append(self.mutation(child2, mutation_prob))
            
            new_population.extend(elites)
            self.population = new_population
            random.shuffle(self.population[elite_count:])
            
            # Track and visualize progress
            best_genome = min(self.population, key=self.calculate_total_distance)
            best_distance = self.calculate_total_distance(best_genome)
            print(best_distance)
            best_distances.append(best_distance)

            ax1.clear()
            ax1.plot(range(len(best_distances)), best_distances, color='b', linestyle='-', linewidth=1)
            ax1.set_title("Distance Evolution")
            ax1.set_xlabel("Generation")
            ax1.set_ylabel("Best Distance")
            ax1.grid(True)

            ax2.clear()
            x = [city.x for city in best_genome] + [best_genome[0].x]
            y = [city.y for city in best_genome] + [best_genome[0].y]
            ax2.plot(x, y, marker='o', label='Route')
            ax2.set_title("TSP Route")
            ax2.set_xlabel("X Coordinate")
            ax2.set_ylabel("Y Coordinate")
            ax2.legend()

            plt.pause(0.1)

        best_genome = min(self.population, key=self.calculate_total_distance)
        best_distance = self.calculate_total_distance(best_genome)
        
        print("\n=== Final Results ===")
        print(f"Best distance found: {best_distance:.2f}")
        print("Best route:")
        
        for i, city in enumerate(best_genome):
            print(f"{i+1}. {city}")
        print(f"{len(best_genome)+1}. {best_genome[0]} (return to start)")

        plt.ioff()
        plt.show()