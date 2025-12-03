from Camera import Camera
import matplotlib.pyplot as plt
from Room import Room
import numpy as np

def main():
        # --- ZONE DE TEST 2 : ROOM + CAMERAS ---

    # 1. Création de la pièce (forme en L)
    shape_L = [(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)]
    my_room = Room(shape_L)

    # 2. Création de quelques caméras
    # Caméra 1 : Coin bas-gauche, regarde vers le haut-droite (45°), FOV 90°, rayon 8
    cam1 = Camera(x=0, y=0, orientation_deg=45, fov_deg=45, radius=6)

    # Caméra 2 : Coin haut-droite du L, regarde vers le bas (-90°), FOV large 120°, rayon 6
    cam2 = Camera(x=10, y=5, orientation_deg=-90, fov_deg=90, radius=6)

    cameras = [cam1, cam2]

    # 3. Préparation du graphique
    fig, ax = plt.subplots(figsize=(8, 8))
    my_room.plot_room(ax)

    # 4. Affichage des caméras
    for cam in cameras:
        cam.plot_camera(ax)

    # 5. Test de visibilité combiné
    # Générons des points aléatoires et voyons s'ils sont vus par AU MOINS UNE caméra
    num_test_points = 200
    np.random.seed(42) # Pour avoir toujours les mêmes points lors des tests

    for _ in range(num_test_points):
        # Génère un point dans les limites du graphique
        tx = np.random.uniform(my_room.bounds[0], my_room.bounds[1])
        ty = np.random.uniform(my_room.bounds[2], my_room.bounds[3])
        test_point = (tx, ty)

        # Logique de couverture :
        # Le point doit être DANS la pièce ET vu par au moins une caméra
        if my_room.is_point_inside(test_point):
            is_seen = False
            for cam in cameras:
                if cam.is_point_visible(test_point):
                    is_seen = True
                    break # Pas besoin de vérifier les autres si une le voit
            
            color = 'green' if is_seen else 'red'
            marker = '.' if is_seen else 'x'
            ax.plot(tx, ty, marker=marker, color=color, markersize=8 if not is_seen else 5, alpha=0.6)

    ax.set_title("Pièce avec 2 caméras et test de couverture")
    plt.show()

if __name__ == "__main__":
    main()