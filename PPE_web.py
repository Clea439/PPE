from Database import database
from Regression import regression
from Mapping import mapping
import pandas as pd

df=pd.read_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\Untitled Folder\regression.csv')
d=database('C:/Users/lilia/OneDrive/Documents/Lilian/ING4_S2/Untitled Folder/Clean2gether.json')

r=regression(df)
mlr=pd.DataFrame(columns=["mlr_lat","mlr_long",'r2_lat','r2_long'])

for i in range(1000):
    mlrlat,r2lat,rmselat,y_pred_mlrlat,y_trainlat=r.lat_reg()
    mlrlong,r2long,rmselong,y_pred_mlrlong,y_trainlong,x_test=r.long_reg()
    mlr=mlr.append({"mlr_lat" :mlrlat ,"mlr_long" : mlrlong, 'r2_lat' :float(r2lat), 'r2_long' :float(r2long) } , ignore_index=True)

best_mlr_lat = mlr['mlr_lat'][mlr["r2_lat"].idxmax()]
best_mlr_long = mlr['mlr_long'][mlr["r2_long"].idxmax()]
best_r2lat = mlr['r2_lat'][mlr["r2_lat"].idxmax()]
best_r2long = mlr['r2_long'][mlr["r2_long"].idxmax()]


print(best_r2lat)
print(best_r2long)

"""
plot the total predictions thanks to the Clean2Gether dataset
"""

train=pd.DataFrame()
train["latitude"]=y_trainlat
train["longitude"]=y_trainlong
train=train.dropna()

m=mapping(y_pred_mlrlong,y_pred_mlrlat)

c=m.create_map_total_prediction(train)

c.save("map_total_prediction.html")


"""
plot the predictions thanks to the epci
"""

finder=d.find_thx_epci("CA du Grand Angoulême", df)

pred_lat=mlrlat.predict(finder)
pred_long=mlrlong.predict(finder)

m=mapping(pred_long,pred_lat)

c=m.create_map_prediction()

c.save("map_prediction_finder_epci.html")


"""
plot the predictions thanks to the county
"""

finder=d.find_thx_county("Charente", df)

pred_lat=mlrlat.predict(finder)
pred_long=mlrlong.predict(finder)

m=mapping(pred_long,pred_lat)

c=m.create_map_prediction()
   
c.save("map_prediction_finder_county.html")
