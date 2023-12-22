import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Date de début et de fin
date_debut = datetime(2023, 1, 1)
date_fin = datetime(2023, 12, 31)

# Liste pour stocker les dates
liste_dates = []

# Boucle pour générer les dates
while date_debut <= date_fin:
    liste_dates.append(date_debut.strftime("%Y-%m-%d"))
    date_debut += timedelta(days=1)

# Load the datasets
file_path_opti = 'simulation_opti.xlsx'
file_path_brut = 'simulation_vidage_brut.xlsx'

data_opti = pd.read_excel(file_path_opti)
data_brut = pd.read_excel(file_path_brut)

# Merge the two DataFrames on common columns (assuming 'Commune' and 'Date' are common columns)
merged_data = pd.merge(data_opti, data_brut, on=['Commune', 'Date'], how='inner')

# Display the first few rows of the merged dataset to understand its structure
communes = merged_data['Commune'].unique()

donnees_opti = {}
donnees_brut = {}

for commune in communes:
    donnees_opti[commune] = 0
    donnees_brut[commune] = 0

# Parcourir les communes et les dates pour compter les jours de vidage pour chaque ensemble de données
for commune in communes:
    nb_jours_opti = 0
    nb_jours_brut = 0
    for jour in liste_dates:
        condition_opti = (merged_data['Commune'] == commune) & (merged_data['Date'] == jour) & (merged_data['Remplissage_x'] == 0)
        condition_brut = (merged_data['Commune'] == commune) & (merged_data['Date'] == jour) & (merged_data['Remplissage_y'] == 0)
        
        if merged_data[condition_opti].shape[0] > 0:
            nb_jours_opti += 1
        if merged_data[condition_brut].shape[0] > 0:
            nb_jours_brut += 1
    
    donnees_opti[commune] = nb_jours_opti
    donnees_brut[commune] = nb_jours_brut

# Liste des clés
liste_des_cles_opti = list(donnees_opti.keys())
liste_des_cles_brut = list(donnees_brut.keys())

# Liste des valeurs
liste_des_valeurs_opti = list(donnees_opti.values())
liste_des_valeurs_brut = list(donnees_brut.values())

plt.figure(figsize=(12, 6))

# Largeur des barres
bar_width = 0.4

# Créez une liste d'indices pour les communes
indices = range(len(liste_des_cles_opti))

# ... (votre code pour charger les données et préparer les données va ici) ...

# Créez un graphique à barres avec deux barres côte à côte pour chaque commune
plt.figure(figsize=(12, 6))

# Largeur des barres
bar_width = 0.4

# Créez une liste d'indices pour les communes
indices = range(len(liste_des_cles_opti))

# Créez deux ensembles de barres pour "Optimisé" (bleu) et "Brut" (vert)
plt.barh([i - bar_width / 2 for i in indices], liste_des_valeurs_opti, bar_width, color='skyblue', label='Optimisé')
plt.barh([i + bar_width / 2 for i in indices], liste_des_valeurs_brut, bar_width, color='orange', label='Brut', alpha=0.7)

# Utilisez les noms de communes pour l'axe des ordonnées
plt.yticks(indices, liste_des_cles_opti)

plt.xlabel('Nombre de jours de passage')
plt.ylabel('Commune')
plt.title('Nombre de jours de passage par commune en 2023')
plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher la commune avec le plus de jours en haut

# Ajouter une zone rouge entre les abscisses 260 et 365
plt.axvspan(260, 365, color='red', alpha=0.5)  # Utilisation de axvspan pour créer la zone rouge

plt.xlim(0, 365)
plt.legend()
plt.tight_layout()

# Afficher le graphique
plt.show()
