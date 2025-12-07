import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class Room:
    def __init__(self, corners, sample_step=1.0):
        """
        Définit une pièce par une liste de coordonnées de ses coins.
        L'ordre des points est important (sens horaire ou anti-horaire).
        corners: liste de tuples [(x1,y1), (x2,y2), ...]
        sample_step: l'espacement entre les points d'échantillonnage
        """
        # On s'assure que c'est un tableau numpy pour faciliter les calculs futurs
        self.corners = np.array(corners)
        
        # Pour fermer le polygone lors du dessin, on répète le premier point à la fin
        self.plot_corners = np.vstack([self.corners, self.corners[0]])

        # Calcul des limites pour le graphique (min_x, max_x, min_y, max_y)
        self.bounds = (
            np.min(self.corners[:, 0]), np.max(self.corners[:, 0]),
            np.min(self.corners[:, 1]), np.max(self.corners[:, 1])
        )
        
        # Génération des points d'échantillonnage
        self.sample_step = sample_step
        self.sample_points = self.generate_sample_points(sample_step)

    def is_point_inside(self, point):
        """
        Algorithme "Ray Casting" pour vérifier si un point (x,y) est dans le polygone.
        Retourne True si le point est dedans, False sinon.
        """
        x, y = point
        n = len(self.corners)
        inside = False
        p1x, p1y = self.corners[0]
        for i in range(n + 1):
            p2x, p2y = self.corners[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1y, p2y = p2x, p2y # Correction ici: il faut mettre à jour p1 pour le tour suivant
            p1x, p1y = p2x, p2y # La bonne mise à jour des variables

        return inside
    
    def generate_sample_points(self, step=1.0):
        """
        Génère une grille de points fixes à l'intérieur de la pièce.
        step: l'espacement entre les points (plus c'est petit, plus c'est précis, mais plus c'est lent).
        """
        points = []
        # On parcourt la "bounding box" de la pièce
        min_x, max_x, min_y, max_y = self.bounds
        
        # arange permet de créer des séquences de nombres avec un pas décimal
        x_range = np.arange(min_x, max_x, step)
        y_range = np.arange(min_y, max_y, step)
        
        for x in x_range:
            for y in y_range:
                # On ajoute le point seulement s'il est vraiment DANS la pièce
                # On ajoute un petit décalage (step/2) pour centrer le point dans sa case virtuelle
                p = (x + step/2, y + step/2)
                if self.is_point_inside(p):
                    points.append(p)
                    
        return np.array(points)

    def plot_room(self, ax):
        """
        Dessine la pièce sur un axe matplotlib donné.
        ax: l'objet 'axes' de matplotlib sur lequel dessiner.
        """
        # Création du polygone
        poly = patches.Polygon(self.corners, closed=True, edgecolor='black', facecolor='#EDEFD0', linewidth=2)
        ax.add_patch(poly)
        
        # Réglage des limites du graphique pour bien voir toute la pièce + une petite marge
        margin = 1
        ax.set_xlim(self.bounds[0] - margin, self.bounds[1] + margin)
        ax.set_ylim(self.bounds[2] - margin, self.bounds[3] + margin)
        ax.set_aspect('equal') # Important pour que les carrés ne ressemblent pas à des rectangles
        ax.set_title("Environment de la pièce")
        ax.grid(True, linestyle='--', alpha=0.6)

    def get_room(self, id_room):
        """
        Retourne une instance de Room prédéfinie selon l'ID.
        id_room: entier identifiant la pièce (1, 2, 3, ...)
        """
        if id_room == 1:
            # Pièce carrée simple
            return Room([(0, 0), (10, 0), (10, 10), (0, 10)])
        elif id_room == 2:
            # Pièce rectangulaire avec une découpe
            return Room([(0, 0), (15, 0), (15, 5), (10, 5), (10, 10), (0, 10)])
        elif id_room == 3:
            # Pièce en L
            return Room([(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)])
        else:
            raise ValueError("ID de pièce inconnu. Veuillez choisir entre 1, 2 ou 3.")