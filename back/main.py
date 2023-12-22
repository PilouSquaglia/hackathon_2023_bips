import requests
import csv
import googlemaps
from fastapi import *

app = FastAPI()




#DAte  a recuperer






import pandas as pd
import json

def create_json_for_date(df, target_date):
   json_data = {}
   idx = 1
   df = df[df['Date'] == target_date]
   

   #json_data['start'] = (42.60080491507166,9.322923935409024)
    
   new_df = df[(df['Coeff_Touriste'] == 3) | ((df['Coeff_Touriste'] == 2) & (df['Remplissage'] >= 30)) | (df['Remplissage'] >= 60)]

   liste_communes = new_df['Commune'].unique()
   return liste_communes





def obtenir_url_itineraire(points, depart, arrivee, cle_api):
    waypoints = '|'.join([f"{point[0]},{point[1]}" for point in points])
    depart_str = f"{depart[0]},{depart[1]}"
    arrivee_str = f"{arrivee[0]},{arrivee[1]}"
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={depart_str}&destination={arrivee_str}&waypoints={waypoints}&key={cle_api}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        # Construire l'URL de l'itinéraire
        itineraire_url = f"https://www.google.com/maps/dir/?api=1&origin={depart_str}&destination={arrivee_str}&waypoints={waypoints}"
        return itineraire_url
    else:
        print("Erreur lors de la récupération de l'itinéraire")
        return None


#with open('data_commune_2023-01-15.json', 'r') as fichier_json:
 #   Chargez le contenu du fichier JSON dans un dictionnaire Python
  #  data = json.load(fichier_json)








@app.get("/travelling")
def get_travelling_json(date):
    lieux = {'olmeta di tuda':(42.612518384347624, 9.355937442006228), 
     'rapale':(42.59044735633119, 9.304493137651338), 
     'santu petro di tenda':(42.60470238743363, 9.258848751457322), 
     'BARBAGGIO':(42.679206404175254, 9.372782802175832), 
     'sorio':(42.58453452791634, 9.273053724997334),
     'pieve':(42.5804313095914, 9.28751927579814), 
     'oletta':(42.631474880100775, 9.355938773719837), 
     'saint florent ':(42.6812407194571, 9.303134444721932), 
     'poggio oletta':(42.63989419060523, 9.358873956697366), 
     'vallecalle':(42.59883299912047, 9.33868388159885), 
     'rutali':(42.5799801123768, 9.364394702267907),
     'farinole':(42.72849435412508, 9.361458373094244), 
     'murato':(42.577729036255576, 9.327092369406772), 
     'patrimonio':(42.70624581822988, 9.370492797889394), 
     'casta':(42.660000, 9.242500),
     'san gavino di tenda':(42.59865647254949, 9.26570637912313)}
    df = pd.read_excel('final_data.xlsx')

    points = create_json_for_date(df,date)
    
    geo = []

    for key, value in lieux.items():
        if key in points:
            geo.append(value)

    # 'data' est maintenant un dictionnaire Python contenant le contenu du fichier JSON
    cle_api_google_maps = "AIzaSyD7j8Srn-xDdT0SUTvH_tt9-YWO-wwjPHI"
    gmaps = googlemaps.Client(key=cle_api_google_maps)



    itineraire = gmaps.directions(
            origin=(42.60080491507166, 9.322923935409024),
            destination=(42.60180491507166, 9.323923935409024),
            waypoints=geo,  # Exclut le point de départ et d'arrivée
            optimize_waypoints=True,  # Optimise l'ordre des waypoints pour le plus court itinéraire
            mode='driving'  # Mode de transport (peut être 'driving', 'walking', 'bicycling', etc.)
      )
    


    waypoint_order = itineraire[0]['waypoint_order']
    

    # Obtenez les noms des communes correspondant à l'ordre des waypoints
    communes_ordre = [list(lieux.keys())[idx] for idx in waypoint_order]
    
    result_json = {}
    for commune in communes_ordre:
        if commune in lieux:
            result_json[commune] = lieux[commune]

    # Créez une réponse JSON avec le résultat
    return result_json

#print(get_travelling_json("2023-01-02"))




  
