# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:47:56 2023

@author: lluca
"""

import pandas as pd
import json

def create_json_for_date(df, target_date):
   json_data = {}
   idx = 1
   df = df[df['Date'] == target_date]
   
   json_data['start'] = (42.60080491507166,9.322923935409024)
    
   new_df = df[(df['Coeff_Touriste'] == 3) | ((df['Coeff_Touriste'] == 2) & (df['Remplissage'] >= 30)) | (df['Remplissage'] >= 60)]

   liste_communes = new_df['Commune'].unique()
   return liste_communes
   for commune in liste_communes:
       json_data[idx] = {'Commune': commune}
       idx += 1
    
   #for commune in liste_communes:
    #df_commune = df[(df['Commune'] == commune) & ((df['Remplissage'] > 10) | (df['Coeff_Touriste'] == 3))]
    
    #for index, row in df_commune.iterrows():
     #json_data[idx] = {'Latitude': row['Latitude'], 'Longitude': row['Longitude']}
     #idx += 1

   # Enregistrer le JSON dans un fichier
   nom_fichier = f"data_commune_{target_date}.json"
   with open(nom_fichier, 'w') as json_file:
       json.dump(json_data, json_file, indent=3)
    
   print(f"Le fichier JSON '{nom_fichier}' a été créé avec succès.")
            
    
    
# Exemple d'utilisation
df = pd.read_excel('final_data.xlsx')
dates = ["2023-01-17","2023-01-16","2023-01-15","2023-09-14","2023-01-13","2023-01-12","2023-01-11"]
for date in dates:   
    create_json_for_date(df, date)
