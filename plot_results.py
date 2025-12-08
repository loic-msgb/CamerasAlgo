"""
Script pour visualiser les résultats du fichier CSV
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_csv_results(csv_file='genetic_algorithm_results.csv'):
    """
    Charge et affiche les résultats du fichier CSV
    """
    # Charger les données
    df = pd.read_csv(csv_file)
    
    print(f"Nombre total d'exécutions : {len(df)}")
    print("\n" + "="*60)
    print("Statistiques globales :")
    print("="*60)
    print(df[['final_max_score', 'final_min_score', 'final_avg_score', 'final_std_score']].describe())
    
    # Créer les graphiques
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Évolution des scores max au fil des exécutions
    ax1 = axes[0, 0]
    ax1.plot(df.index, df['final_max_score'], marker='o', linestyle='-', linewidth=2, markersize=6)
    ax1.set_xlabel('Numéro d\'exécution')
    ax1.set_ylabel('Score maximum (%)')
    ax1.set_title('Évolution du meilleur score')
    ax1.grid(True, alpha=0.3)
    
    # 2. Comparaison des statistiques (box plot)
    ax2 = axes[0, 1]
    data_to_plot = [df['final_max_score'], df['final_avg_score'], df['final_min_score']]
    bp = ax2.boxplot(data_to_plot, labels=['Maximum', 'Moyenne', 'Minimum'])
    ax2.set_ylabel('Score (%)')
    ax2.set_title('Distribution des scores finaux')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Impact du taux de mutation (si variable)
    ax3 = axes[1, 0]
    if df['mutation_rate'].nunique() > 1:
        scatter = ax3.scatter(df['mutation_rate'], df['final_max_score'], 
                            c=df['mutation_strength'], cmap='viridis', 
                            s=100, alpha=0.6, edgecolors='black')
        ax3.set_xlabel('Taux de mutation')
        ax3.set_ylabel('Score maximum (%)')
        ax3.set_title('Impact du taux de mutation')
        plt.colorbar(scatter, ax=ax3, label='Force de mutation')
    else:
        ax3.plot(df.index, df['final_avg_score'], marker='s', linestyle='--', 
                linewidth=2, markersize=6, color='orange', label='Moyenne')
        ax3.plot(df.index, df['final_max_score'], marker='o', linestyle='-', 
                linewidth=2, markersize=6, color='green', label='Maximum')
        ax3.fill_between(df.index, df['final_min_score'], df['final_max_score'], 
                        alpha=0.2, color='blue')
        ax3.set_xlabel('Numéro d\'exécution')
        ax3.set_ylabel('Score (%)')
        ax3.set_title('Évolution des scores (Min/Avg/Max)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # 4. Impact de la taille de population (si variable)
    ax4 = axes[1, 1]
    if df['pop_size'].nunique() > 1:
        for pop_size in df['pop_size'].unique():
            subset = df[df['pop_size'] == pop_size]
            ax4.scatter(subset['generations'], subset['final_max_score'], 
                       label=f'Pop={int(pop_size)}', s=100, alpha=0.6)
        ax4.set_xlabel('Nombre de générations')
        ax4.set_ylabel('Score maximum (%)')
        ax4.set_title('Impact de la taille de population')
        ax4.legend()
    else:
        # Graphique de l'écart-type
        ax4.plot(df.index, df['final_std_score'], marker='d', linestyle=':', 
                linewidth=2, markersize=6, color='red')
        ax4.set_xlabel('Numéro d\'exécution')
        ax4.set_ylabel('Écart-type (%)')
        ax4.set_title('Diversité de la population finale')
        ax4.grid(True, alpha=0.3)
    
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Afficher le tableau des résultats
    print("\n" + "="*60)
    print("Résumé des exécutions :")
    print("="*60)
    cols_to_show = ['timestamp', 'num_cameras', 'pop_size', 'generations', 
                    'mutation_rate', 'final_max_score', 'final_avg_score', 'final_std_score']
    print(df[cols_to_show].to_string(index=False))

if __name__ == "__main__":
    plot_csv_results()
