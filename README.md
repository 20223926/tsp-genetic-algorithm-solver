# TSP Genetic Algorithm Solver

A Python project that solves the Travelling Salesman Problem (TSP) using a genetic algorithm. Cities are placed randomly on a 2D map, and the algorithm evolves a population of routes to find a short tour that visits each city once and returns to the start.

## Features

- Configurable population size, generations, mutation rate, and elitism
- Parent selection: tournament or roulette wheel
- Crossover operators: Order Crossover (OX), Order One Crossover (OX1), Partially Mapped Crossover (PMX)
- Live plots of distance evolution and the best route found so far

## Requirements

- Python 3
- `matplotlib`

## Usage

```bash
python main.py
```

You can press Enter at each prompt to keep the default values, or set your own parameters interactively.
