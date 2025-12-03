import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def normalize_angle(angle):
    """
    Utilitaire pour ramener un angle (en radians) entre -pi et +pi.
    C'est crucial pour comparer des angles autour du cercle.
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

class Camera:
    def __init__(self, x, y, orientation_deg, fov_deg, radius):
        self.x = x
        self.y = y
        # On convertit tout en radians pour les calculs numpy
        self.orientation = np.radians(orientation_deg)
        self.fov = np.radians(fov_deg)
        self.radius = radius
        
        # Calcul des angles de début et de fin du cône (pour le dessin)
        # Matplotlib attend des degrés pour les Wedges
        self.theta1_deg = orientation_deg - (fov_deg / 2)
        self.theta2_deg = orientation_deg + (fov_deg / 2)

    def is_point_visible(self, point):
        """
        Vérifie si un point (tx, ty) est dans le cône de vision de la caméra.
        """
        tx, ty = point
        dx = tx - self.x
        dy = ty - self.y

        # 1. Vérification de la distance (Pythagore au carré pour éviter la racine carrée, c'est plus rapide)
        dist_sq = dx*dx + dy*dy
        if dist_sq > self.radius*self.radius:
            return False # Trop loin

        # 2. Vérification de l'angle
        # atan2 calcule l'angle du point par rapport à l'axe X (entre -pi et +pi)
        angle_to_point = np.arctan2(dy, dx)
        
        # On calcule la différence entre l'angle du point et l'orientation de la caméra
        angle_diff = normalize_angle(angle_to_point - self.orientation)
        
        # Si cette différence est inférieure à la moitié du FOV, c'est dedans !
        if np.abs(angle_diff) <= (self.fov / 2):
            return True
            
        return False

    def plot_camera(self, ax):
        """ Dessine la caméra (un point) et son cône (un Wedge) """
        # Le cône de vision (Wedge = part de camembert)
        # alpha gère la transparence
        wedge = patches.Wedge((self.x, self.y), self.radius, 
                              self.theta1_deg, self.theta2_deg, 
                              color='blue', alpha=0.3)
        ax.add_patch(wedge)
        
        # Le point central de la caméra
        ax.plot(self.x, self.y, marker='o', color='black', markersize=5)