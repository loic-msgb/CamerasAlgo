import random
from Camera import Camera

class Individual:
    def __init__(self, room, num_cameras, fov, radius, genes=None):
        self.room = room
        self.num_cameras = num_cameras
        self.fov = fov
        self.radius = radius
        self.fitness = None
        
        if genes is None:
            # Création aléatoire (Naissance)
            self.genes = []
            for _ in range(num_cameras):
                # On cherche un point valide dans la pièce
                # On essaie tant qu'on n'est pas dedans (méthode un peu brute mais efficace)
                while True:
                    x = random.uniform(room.bounds[0], room.bounds[1])
                    y = random.uniform(room.bounds[2], room.bounds[3])
                    if room.is_point_inside((x, y)):
                        angle = random.uniform(0, 360)
                        self.genes.append([x, y, angle])
                        break
        else:
            # Création à partir de gènes existants (Enfant)
            self.genes = genes

    def get_cameras(self):
        """ Transforme l'ADN (chiffres) en objets Camera utilisables """
        cameras = []
        for gene in self.genes:
            x, y, angle = gene
            cameras.append(Camera(x, y, angle, self.fov, self.radius))
        return cameras
    
    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness
    
    def crossover(self, other_parent):
        """ Uniform Crossover : Pile ou face pour chaque gène """
        child1_genes = []
        child2_genes = []
        
        for i in range(self.num_cameras):
            if random.random() < 0.5:
                # Cas A : On garde l'ordre
                child1_genes.append(self.genes[i])
                child2_genes.append(other_parent.genes[i])
            else:
                # Cas B : On inverse
                child1_genes.append(other_parent.genes[i])
                child2_genes.append(self.genes[i])
                
        return (
            Individual(self.room, self.num_cameras, self.fov, self.radius, child1_genes),
            Individual(self.room, self.num_cameras, self.fov, self.radius, child2_genes)
    )

    def mutate(self, mutation_rate, mutation_strength):
        """
        Mutation : Avec une petite probabilité, on déplace un peu une caméra.
        mutation_rate : Chance qu'une caméra mute (ex: 0.1 pour 10%)
        mutation_strength : De combien on bouge (ex: 1.0 mètre)
        """
        new_genes = []
        for gene in self.genes:
            x, y, angle = gene
            
            # Test de mutation
            if random.random() < mutation_rate:
                # On modifie légèrement x et y
                x += random.uniform(-mutation_strength, mutation_strength)
                y += random.uniform(-mutation_strength, mutation_strength)
                
                # On modifie l'angle
                angle += random.uniform(-20, 20) # +/- 20 degrés
                
                # IMPORTANT : On vérifie si la caméra est sortie de la pièce.
                # Si elle est sortie, on annule le mouvement (ou on la remet au bord).
                # Ici, on annule simplement la mutation spatiale si invalide.
                if not self.room.is_point_inside((x, y)):
                    x, y = gene[0], gene[1] # On revient à l'ancienne position
            
            new_genes.append([x, y, angle])
            
        self.genes = new_genes