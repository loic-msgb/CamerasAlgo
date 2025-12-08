import random
import numpy as np
from Camera import Camera
from Room import Room
from Individual import Individual

def calculate_fitness(room: Room, individual: Individual):
    """
    Calcule le pourcentage de points couverts par les caméras d'un individu.
    room: la Room contenant les points d'échantillonnage
    individual: l'individu dont on évalue les caméras (ou liste de caméras)
    Retourne un float entre 0.0 (0%) et 1.0 (100%).
    """
    sample_points = room.sample_points
    
    if len(sample_points) == 0:
        return 0.0
    
    # Récupère les caméras de l'individu à partir de ses gènes
    # Gère aussi le cas où on passe directement une liste de caméras
    if isinstance(individual, Individual):
        cameras = individual.get_cameras()
    else:
        cameras = individual
    covered_count = 0
    
    for point in sample_points:
        is_covered = False
        # Vérifie si le point est vu par au moins UNE caméra
        for cam in cameras:
            if cam.is_point_visible(point):
                is_covered = True
                break # Optimisation : dès qu'une caméra le voit, on passe au point suivant
        
        if is_covered:
            covered_count += 1
            
    return covered_count / len(sample_points)


def select_parent(population, k=3):
    """
    Sélection par tournoi simple : prend k individus au hasard et retourne le meilleur.
    """
    selected = random.sample(population, k)
    return max(selected, key=lambda ind: ind.fitness)


def roulette_wheel_selection(population):
    """
    Sélection par roulette : probabilité proportionnelle à la fitness.
    Gère les cas où la fitness totale est nulle ou négative.
    """
    total_fitness = sum(individual.fitness for individual in population)
    
    # Si toutes les fitness sont nulles ou négatives, sélection uniforme
    if total_fitness <= 0:
        return random.choice(population)
    
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual in population:
        current += individual.fitness
        if current > pick:
            return individual
    return population[-1]  # Fallback


def rank_selection(population: list):
    """
    Sélection par rang : attribue un rang à chaque individu et choisit en fonction de ce rang.
    Probabilité linéaire : meilleur individu a le poids le plus élevé.
    """
    # Use pre-calculated fitness to assign ranks
    ranked_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
    n = len(ranked_population)
    
    # Poids linéaire : rang 0 (meilleur) -> poids n, rang (n-1) (pire) -> poids 1
    # Somme des poids = n + (n-1) + ... + 1 = n(n+1)/2
    weights = [n - rank for rank in range(n)]
    selected_index = random.choices(range(n), weights=weights, k=1)[0]
    return ranked_population[selected_index]


def run_genetic_algorithm(
    room: Room,
    num_cameras: int,
    pop_size: int = 20,
    generations: int = 30,
    fov: float = 90,
    radius: float = 12,
    mutation_rate: float = 0.2,
    mutation_strength: float = 1.5,
):
    """
    Évolution génétique :
    - Conserve la meilleure moitié de la population (élitisme fort).
    - Complète l'autre moitié avec de nouveaux enfants issus de croisements/mutations.
    - Les parents sont re-sélectionnés à chaque création d'enfant dans la génération A.
    Retourne le meilleur individu rencontré et l'historique des meilleurs scores.
    """

    # Génération 0
    population = [Individual(room, num_cameras, fov, radius) for _ in range(pop_size)]
    best_scores = []
    min_scores = []
    avg_scores = []
    std_scores = []
    best_individual = None
    best_fitness = -1.0

    for _ in range(generations):
        # A. Évaluation
        for ind in population:
            if ind.fitness is None:
                ind.set_fitness(calculate_fitness(room, ind))

        # B. Tri du meilleur au moins bon
        population.sort(key=lambda ind: ind.fitness, reverse=True)

        # Mise à jour du meilleur global
        if population[0].fitness > best_fitness:
            best_fitness = population[0].fitness
            best_individual = population[0]

        # Calcul des statistiques de la population
        fitness_values = [ind.fitness for ind in population]
        best_scores.append(population[0].fitness)
        min_scores.append(min(fitness_values))
        avg_scores.append(np.mean(fitness_values))
        std_scores.append(np.std(fitness_values))

        # C. Nouvelle génération
        survivors_count = pop_size // 2  # meilleure moitié
        next_gen = population[:survivors_count]  # copie directe des meilleurs

        # Remplissage avec de nouveaux enfants
        while len(next_gen) < pop_size:
            parent_a = roulette_wheel_selection(population)
            parent_b = roulette_wheel_selection(population)

            child1, child2 = parent_a.crossover(parent_b)
            child1.mutate(mutation_rate=mutation_rate, mutation_strength=mutation_strength)
            child2.mutate(mutation_rate=mutation_rate, mutation_strength=mutation_strength)

            next_gen.append(child1)
            if len(next_gen) < pop_size:
                next_gen.append(child2)

        population = next_gen

    # Créer un dictionnaire avec toutes les statistiques
    stats = {
        'best_scores': best_scores,
        'min_scores': min_scores,
        'avg_scores': avg_scores,
        'std_scores': std_scores
    }
    
    return best_individual, stats