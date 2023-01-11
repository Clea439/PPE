from SannoisDatabase import database
from RegressionSannois import RegressionSannois
from Mapping import mapping
import pandas as pd

d=database('sannois_depot_sauvage.csv')

data = d.create_data()

r=RegressionSannois(data)

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
mlr_type, y_trainType, AccuracyScore=r.type()

# Ajout de la prédiction du type à notre dataframe
type = (y_trainType, pd.DataFrame(mlr_type))
types = pd.concat(type,axis=0)
frames = (result, types)
result = pd.concat(frames,axis=1)
result.columns = ['Longitude','Latitude', 'Type']

# Prédiction du poids
mlr_tonnage,y_trainTonnage,r2Type,rmseType=r.tonnage(result)

# Ajout de la prédiction du poids à notre dataframe
tonnage = (y_trainTonnage, pd.DataFrame(mlr_tonnage))
tonnages = pd.concat(tonnage,axis=0)
frames = (result, tonnages)
result = pd.concat(frames,axis=1)
result.columns = ['Longitude','Latitude', 'Type','Tonnage']

# Prédiction du Prix
price,y_trainPrix,r2Price,rmsePrice = r.price(result)

# Ajout de la prédiction du prix à notre dataframe
prix = (y_trainPrix, pd.DataFrame(price))
prix = pd.concat(prix,axis=0)
frames = (result, prix)
result = pd.concat(frames,axis=1)
result.columns = ['Longitude','Latitude', 'Type','Tonnage', 'Prix']
print(result)


#print("LongitudeR:"+str(y_testlong) + "LatitudeR:"+str(y_testlat))
#print("R2 (Coefficient of determination) is a measure of the goodness of fit of a model.")
#print("")
print("Coefficient of determination for the latitude : "+str(r2lat*100)+" %")
print("Coefficient of determination for the longitude : "+str(r2long*100)+" %")
print("Coefficient of determination for the tonnage : "+str(r2Type*100)+" %")
print("Coefficient of determination for the type : "+str(AccuracyScore*100)+" %")
print("Coefficient of determination for the Price : "+str(r2Price*100)+" %")

