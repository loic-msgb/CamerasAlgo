from Camera import Camera
import matplotlib.pyplot as plt
from Room import Room
import numpy as np
import csv
import os
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
    generations = 3000
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
    best_individual, stats = run_genetic_algorithm(
        room=my_room,
        num_cameras=num_cameras,
        pop_size=pop_size,
        generations=generations,
        fov=fov,
        radius=radius,
        mutation_rate=mutation_rate,
        mutation_strength=mutation_strength
    )
    
    # Extraire les statistiques finales
    best_scores = stats['best_scores']
    final_best = best_scores[-1] * 100
    final_min = stats['min_scores'][-1] * 100
    final_avg = stats['avg_scores'][-1] * 100
    final_std = stats['std_scores'][-1] * 100
    
    print(f"\nStatistiques finales de la population :")
    print(f"  - Meilleur score : {final_best:.2f}%")
    print(f"  - Score minimum : {final_min:.2f}%")
    print(f"  - Score moyen : {final_avg:.2f}%")
    print(f"  - Écart-type : {final_std:.2f}%")
    print("=" * 60)
    
    # Sauvegarder les résultats dans un fichier CSV commun
    from datetime import datetime
    csv_filename = "genetic_algorithm_results.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Vérifier si le fichier existe pour savoir si on doit écrire l'en-tête
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'timestamp', 'selection_type', 'num_cameras', 'pop_size', 'generations',
            'fov', 'radius', 'mutation_rate', 'mutation_strength', 'elitism_strategy',
            'crossover_type', 'final_max_score', 'final_min_score', 'final_avg_score',
            'final_std_score', 'num_sample_points', 'camera_positions'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête seulement si le fichier est nouveau
        if not file_exists:
            writer.writeheader()
        
        # Préparer les positions des caméras
        cameras = best_individual.get_cameras()
        camera_positions = '; '.join([
            f"C{i+1}(x={cam.x:.2f},y={cam.y:.2f},angle={np.degrees(cam.orientation):.2f})"
            for i, cam in enumerate(cameras)
        ])
        
        # Écrire les données
        writer.writerow({
            'timestamp': timestamp,
            'selection_type': 'Roulette Wheel',
            'num_cameras': num_cameras,
            'pop_size': pop_size,
            'generations': generations,
            'fov': fov,
            'radius': radius,
            'mutation_rate': mutation_rate,
            'mutation_strength': mutation_strength,
            'elitism_strategy': 'Top 50%',
            'crossover_type': 'Uniform',
            'final_max_score': final_best,
            'final_min_score': final_min,
            'final_avg_score': final_avg,
            'final_std_score': final_std,
            'num_sample_points': len(my_room.sample_points),
            'camera_positions': camera_positions
        })
    
    print(f"\nRésultats ajoutés au fichier : {csv_filename}")
    print("=" * 60)
    
    # --- VISUALISATION ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Graphique 1 : Évolution de la fitness avec statistiques
    generations_range = range(len(best_scores))
    ax1.plot(generations_range, [score * 100 for score in best_scores], 
             linewidth=2, label='Maximum', color='green')
    ax1.plot(generations_range, [score * 100 for score in stats['avg_scores']], 
             linewidth=2, label='Moyenne', color='blue', linestyle='--')
    ax1.plot(generations_range, [score * 100 for score in stats['min_scores']], 
             linewidth=2, label='Minimum', color='red', linestyle=':')
    
    # Ajouter une zone d'écart-type
    avg_array = np.array(stats['avg_scores']) * 100
    std_array = np.array(stats['std_scores']) * 100
    ax1.fill_between(generations_range, avg_array - std_array, avg_array + std_array, 
                     alpha=0.2, color='blue', label='±1 écart-type')
    
    ax1.set_xlabel('Génération')
    ax1.set_ylabel('Couverture (%)')
    ax1.set_title('Évolution des statistiques de la population')
    ax1.legend(loc='best')
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