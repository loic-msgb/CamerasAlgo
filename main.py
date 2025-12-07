from Camera import Camera
import matplotlib.pyplot as plt
from Room import Room
import numpy as np
from utils import calculate_fitness, run_genetic_algorithm

def main():
    # --- CONFIGURATION DE LA PIÈCE ---
    shape_L = [(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)]
    my_room = Room(shape_L, sample_step=0.5)
    
    print(f"Nombre de points à vérifier : {len(my_room.sample_points)}")
    print("=" * 60)
    
    # --- PARAMÈTRES DE L'ALGORITHME GÉNÉTIQUE ---
    num_cameras = 3
    pop_size = 50
    generations = 1500
    fov = 45
    radius = 6
    mutation_rate = 0.1
    mutation_strength = 1.0
    
    print(f"Configuration de l'algorithme génétique :")
    print(f"  - Nombre de caméras : {num_cameras}")
    print(f"  - Taille de la population : {pop_size}")
    print(f"  - Nombre de générations : {generations}")
    print(f"  - FOV : {fov}°")
    print(f"  - Rayon : {radius}")
    print(f"  - Taux de mutation : {mutation_rate}")
    print(f"  - Force de mutation : {mutation_strength}")
    print("=" * 60)
    
    # --- EXÉCUTION DE L'ALGORITHME ---
    print("Démarrage de l'algorithme génétique...")
    best_individual, best_scores = run_genetic_algorithm(
        room=my_room,
        num_cameras=num_cameras,
        pop_size=pop_size,
        generations=generations,
        fov=fov,
        radius=radius,
        mutation_rate=mutation_rate,
        mutation_strength=mutation_strength
    )
    
    print(f"\nMeilleur score atteint : {best_individual.fitness * 100:.2f}%")
    print("=" * 60)
    
    # --- VISUALISATION ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Graphique 1 : Évolution de la fitness
    ax1.plot(range(len(best_scores)), [score * 100 for score in best_scores], linewidth=2)
    ax1.set_xlabel('Génération')
    ax1.set_ylabel('Couverture (%)')
    ax1.set_title('Évolution de la meilleure fitness')
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2 : Meilleure configuration
    my_room.plot_room(ax2)
    cameras = best_individual.get_cameras()
    for i, cam in enumerate(cameras):
        cam.plot_camera(ax2)
    ax2.set_title(f'Meilleure configuration ({best_individual.fitness * 100:.2f}% de couverture)')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()