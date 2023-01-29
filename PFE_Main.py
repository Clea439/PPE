from SannoisDatabase import database
from RegressionSannois import RegressionSannois
from Mapping import mapping
import pandas as pd


class Main:
    def __init__(self, d, travaux):
        self.data = d.create_data()
        self.travaux = travaux

    def get_regressions(self):

        r=RegressionSannois(self.data, self.travaux)

        # Prediction Longitude/Latitude
        mlrlat,mlrlong,r2lat,r2long,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat,y_testlat,y_testlong=r.opti_regression()

        # Creation d'une dataframe logitude/latitude de notre prediction
        longitude = (y_trainlong, pd.DataFrame(y_pred_mlrlong))
        longitudes = pd.concat(longitude,axis=0)
        latitude = (y_trainlat, pd.DataFrame(y_pred_mlrlat))
        latitudes = pd.concat(latitude,axis=0)
        frames = (longitudes, latitudes)
        result = pd.concat(frames,axis=1)
        result.columns = ['Longitude','Latitude']

        # Prediction du type de déchet
        mlr_type, y_trainType, y_testType, AccuracyScore=r.type()

        # Ajout de la prédiction du type à notre dataframe
        type = (y_trainType, pd.DataFrame(mlr_type))
        types = pd.concat(type,axis=0)
        frames = (result, types)
        result = pd.concat(frames,axis=1)
        result.columns = ['Longitude','Latitude', 'Type']

        # Prédiction du poids
        mlr_tonnage,y_trainTonnage, y_testTonnage, r2Type,rmseType=r.tonnage(result)

        # Ajout de la prédiction du poids à notre dataframe
        tonnage = (y_trainTonnage, pd.DataFrame(mlr_tonnage))
        tonnages = pd.concat(tonnage,axis=0)
        frames = (result, tonnages)
        result = pd.concat(frames,axis=1)
        result.columns = ['Longitude','Latitude', 'Type','Tonnage']
        
        # Creation de la dataframe permettant d'afficher les prédictions et les valeurs réelles dans la map
        value = (pd.DataFrame(y_pred_mlrlong), pd.DataFrame(y_pred_mlrlat), pd.DataFrame(mlr_type), pd.DataFrame(mlr_tonnage))
        predictions = pd.concat(value,axis=1)
        predictions.columns = ['LongitudePred','LatitudePred', 'TypePred','TonnagePred']
        predictions['Verification'] = 0
        TrueValue = (pd.DataFrame(y_testlong), pd.DataFrame(y_testlat), pd.DataFrame(y_testType), pd.DataFrame(y_testTonnage))
        TrueValue = pd.concat(TrueValue,axis=1)
        TrueValue.columns = ['LongitudeReel','LatitudeReel', 'TypeReel','TonnageReel']


        print("Coefficient of determination for the latitude : "+str(r2lat*100)+" %")
        print("Coefficient of determination for the longitude : "+str(r2long*100)+" %")
        print("Coefficient of determination for the tonnage : "+str(r2Type*100)+" %")
        print("Coefficient of determination for the type : "+str(AccuracyScore*100)+" %")

        return predictions, TrueValue

