# -*- coding: utf-8 -*-
import pandas as pd
import folium
import numpy as np
from datetime import datetime
import geopy.distance



class mapping:
    
    def __init__(self, prediction, trueValue):
                self.prediction = prediction
                self.trueValue = trueValue
                self.dechetteries =pd.read_csv('DECHETTERIE.csv')
                self.dechetteries = self.dechetteries.dropna()

    def CalculDistance(self, longitude, latitude):
            Mindistance = 10000000000000
            MinName = ""
            for i in range(0,len(self.dechetteries)):
                coords_1 = (latitude, longitude)
                coords_2 = (self.dechetteries.iloc[i]['Latitude'], self.dechetteries.iloc[i]['Longitude'])

                if((geopy.distance.geodesic(coords_1, coords_2).km) < Mindistance):

                    Mindistance = (geopy.distance.geodesic(coords_1, coords_2).km)
                    MinName = self.dechetteries.iloc[i]['Name']

            return MinName, Mindistance

    def create_map_prediction(self):
        
           c = folium.Map(location=[ 48.972065, 2.253474])

           for i in range(0,len(self.prediction)):
               cmpt = 0
               type = ""
               tonnage = ""
               self.name, self.distance = self.CalculDistance(self.prediction.iloc[i]['LongitudePred'],self.prediction.iloc[i]['LatitudePred'])
               for j in range(0,len(self.prediction)):
                    if ((self.prediction.iloc[i]['LatitudePred'] == self.prediction.iloc[j]['LatitudePred']) and self.prediction.iloc[i]['LongitudePred'] == self.prediction.iloc[j]['LongitudePred']):
                        if cmpt < 16:
                            cmpt = cmpt+ 1

               if (int(self.prediction.iloc[i]["TypePred"]) == 1):
                    type = "Objet Encombrant"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 2):
                    type = "DIB, ordures Menagères"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 3):
                    type = "Gravats"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 4):
                    type = "Déchets Végétaux"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 5):
                    type = "Protoxyte d'azote"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 6):
                    type = "Amiante"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])
               elif(int(self.prediction.iloc[i]["TypePred"]) == 7):
                    type = "Pneu ou autre objet"
                    tonnage = str(self.prediction.iloc[j]["TonnagePred"])

                
               folium.Circle(
                  location=[self.prediction.iloc[i]['LatitudePred'], self.prediction.iloc[i]['LongitudePred']],
                  radius=np.exp(5),
                  color="red",
                  weight=2,
                  popup=folium.Popup("""<h4 style="color:#0000FF;">Type du déchet : </h4><div style="color:#000000;">"""+str(type)+"""</div>
                                     <h4 style="color:#0000FF;">Poids du déchet : </h4><div style="color:#000000;">"""+str(tonnage)+"""</div>
                                     <h4 style="color:#0000FF;"> Probabilité de déchet à cet endroit: </h4><div style="color:#000000;">"""+str(cmpt*6)+ "%"+"""</div>
                                     <h4 style="color:#0000FF;">Nom de la dechetterie la plus proche : </h4><div style="color:#000000;">"""+str(self.name)+"""</div>
                                     <h4 style="color:#0000FF;">Distance de la déchetterie : </h4><div style="color:#000000;">"""+str(self.distance)+"""</div>
                                     <h4 style="color:#0000FF;">Longitude : </h4><div style="color:#000000;">"""+str(self.prediction.iloc[i]['LongitudePred'])+"""</div>
                                     <h4 style="color:#0000FF;">Latitude : </h4><div style="color:#000000;">"""+str(self.prediction.iloc[i]['LatitudePred'])+"""</div>"""

                                     , max_width=500),
                  fill_color='orange',
                  fill_opacity = 0.2,
               ).add_to(c)
        
           for i in range(0,len(self.trueValue)):
                cmpt = 0
                type = ""
                tonnage = ""
                self.name, self.distance = self.CalculDistance(self.trueValue.iloc[i]['LongitudeReel'], self.trueValue.iloc[i]['LatitudeReel'])
                for j in range(0,len(self.trueValue)):
                    if ((self.trueValue.iloc[i]['LatitudeReel'] == self.trueValue.iloc[j]['LatitudeReel']) and self.trueValue.iloc[i]['LongitudeReel'] == self.trueValue.iloc[j]['LongitudeReel']):
                        cmpt = cmpt+ 1
                        if(type == ""):
                            if (int(self.trueValue.iloc[i]["TypeReel"]) == 1):
                                type = "Objet Encombrant"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 2):
                                type = "DIB, ordures Menagères"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 3):
                                type = "Gravats"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 4):
                                type = "Déchets Végétaux"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 5):
                                type = "Protoxyte d'azote"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 6):
                                type = "Amiante"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                            elif(int(self.trueValue.iloc[i]["TypeReel"]) == 7):
                                type = "Pneu ou autre objet"
                                tonnage = str(self.trueValue.iloc[j]["TonnageReel"])

                        elif (int(self.trueValue.iloc[i]["TypeReel"]) == 1):
                            type = type + ", "+"Objet Encombrant"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 2):
                            type = type + ", "+"DIB, ordures Menagères"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 3):
                            type = type + ", "+"Gravats"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 4):
                            type = type + ", "+"Déchets Végétaux"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 5):
                            type = type + ", "+"Protoxyte d'azote"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 6):
                            type = type + ", "+"Amiante"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])
                        elif(int(self.trueValue.iloc[i]["TypeReel"]) == 7):
                            type = type + ", "+"Pneu ou autre objet"
                            tonnage = tonnage + ", "+str(self.trueValue.iloc[j]["TonnageReel"])

                if(type == ""):
                    if (int(self.trueValue.iloc[i]["TypeReel"]) == 1):
                        type = "Objet Encombrant"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 2):
                        type = "DIB, ordures Menagères"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 3):
                        type = "Gravats"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 4):
                        type = "Déchets Végétaux"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 5):
                        type = "Protoxyte d'azote"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 6):
                        type = "Amiante"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
                    elif(int(self.trueValue.iloc[i]["TypeReel"]) == 7):
                        type = "Pneu ou autre objet"
                        tonnage = str(self.trueValue.iloc[j]["TonnageReel"])
           

                folium.Circle(
                    location=[self.trueValue.iloc[i]['LatitudeReel'], self.trueValue.iloc[i]['LongitudeReel']],
                    radius=np.exp(5),
                    color="black",
                    weight=2,
                    popup=folium.Popup("""<h4 style="color:#000000;">Type du déchet : </h4><div style="color:#000000;">"""+str(type)+"""</div>
                                        <h4 style="color:#000000;">Poids du déchet : </h4><div style="color:#000000;">"""+str(tonnage)+"""</div>
                                        <h4 style="color:#000000;">Nb de déchets à cet endroit  : </h4><div style="color:#000000;">"""+str(cmpt)+"""</div>
                                        <h4 style="color:#000000;">Nom de la dechetterie la plus proche : </h4><div style="color:#000000;">"""+str(self.name)+"""</div>
                                     <h4 style="color:#000000;">Distance de la déchetterie : </h4><div style="color:#000000;">"""+str(self.distance)+"""</div>
                                        <h4 style="color:#000000;">Longitude : </h4><div style="color:#000000;">"""+str(self.trueValue.iloc[i]['LongitudeReel'])+"""</div>
                                        <h4 style="color:#000000;">Latitude : </h4><div style="color:#000000;">"""+str(self.trueValue.iloc[i]['LatitudeReel'])+"""</div>"""
                                        , max_width=500),
                    fill_color='blue',
                    fill_opacity = 0.2,
                ).add_to(c)

                for i in range(0,len(self.dechetteries)):
                    icon_hz = dict(prefix='fa', color='red', icon_color='darkred', icon='cny')
                    folium.Marker([self.dechetteries.iloc[i]['Latitude'], self.dechetteries.iloc[i]['Longitude']], popup = str(self.dechetteries.iloc[i]['Name']),icon=folium.Icon(color='green',icon='trash')).add_to(c)
                    
            
           return c

