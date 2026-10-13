from tsp import TSP
from city import City

def main():
    default_cities_count = 30
    default_population_size = 300
    default_generations_limit = 100
    default_mutation_prob = 0.05
    default_tournament_size = 3
    default_elite_count = 0
    
    print("=== Welcome to the TSP Genetic Algorithm Solver ===")
    print("Press Enter to use default values")
    
    try:
        cities_count_input = input(f"Number of cities [{default_cities_count}]: ")
        cities_count = int(cities_count_input) if cities_count_input else default_cities_count
        if cities_count <= 0:
            raise ValueError("Number of cities must be positive")
        
        population_size_input = input(f"Population size [{default_population_size}]: ")
        population_size = int(population_size_input) if population_size_input else default_population_size
        if population_size <= 0:
            raise ValueError("Population size must be positive")
        
        generations_limit_input = input(f"Generations limit [{default_generations_limit}]: ")
        generations_limit = int(generations_limit_input) if generations_limit_input else default_generations_limit
        if generations_limit <= 0:
            raise ValueError("Generations limit must be positive")
        
        mutation_prob_input = input(f"Mutation probability [{default_mutation_prob}]: ")
        mutation_prob = float(mutation_prob_input) if mutation_prob_input else default_mutation_prob
        if mutation_prob >= 1:
            raise ValueError("Mutation probability must be less than 1")
        elif mutation_prob < 0:
            raise ValueError("Mutation probability must be positive")
        
        print("\nParent selection methods:")
        print("1. Tournament Selection")
        print("2. Roulette Wheel Selection")
        selection_method_input = input("Selection method [1]: ")
        selection_method = int(selection_method_input) if selection_method_input else 1
        
        if selection_method not in [1, 2]:
            raise ValueError("Selection method must be either 1 or 2")
        
        tournament_size = default_tournament_size
        if selection_method == 1:
            tournament_size_input = input(f"Tournament size [{default_tournament_size}]: ")
            tournament_size = int(tournament_size_input) if tournament_size_input else default_tournament_size
        
        print("\nCrossover methods:")
        print("1. Order Crossover (OX)")
        print("2. Order One Crossover (OX1)")
        print("3. Partially Mapped Crossover (PMX)")
        crossover_method_input = input("Crossover method [3]: ")
        crossover_method = int(crossover_method_input) if crossover_method_input else 3
        
        if crossover_method not in [1, 2, 3]:
            raise ValueError("Crossover method must be 1, 2, or 3")
        
        elite_count_input = input(f"Number of elites [{default_elite_count}]: ")
        elite_count = int(elite_count_input) if elite_count_input else default_elite_count
        if elite_count < 0:
            raise ValueError("Number of elites must be positive")
        if elite_count >= population_size:
            raise ValueError("Number of elites must be less than population size")
        
        print("\nGenerating cities and running algorithm...")
        cities = City.generate_random_cities(cities_count=cities_count)
        tsp = TSP(cities_list=cities, population_size=population_size)
        
        tsp.run(generations_limit=generations_limit, 
                mutation_prob=mutation_prob, 
                elite_count=elite_count,
                selection_method=selection_method,
                tournament_size=tournament_size,
                crossover_method=crossover_method)
    except ValueError as e:
        print(f"Error: {e}")
main()