from Database import database
from Regression import regression
from Mapping import mapping
import pandas as pd

df=pd.read_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\PPE\PPE\regression.csv')
d=database('C:/Users/lilia/OneDrive/Documents/Lilian/ING4_S2/PPE/PPE/Clean2gether.json')

r=regression(df)

mlrlat,mlrlong,r2lat,r2long,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat=r.opti_regression()

print(r2lat)
print(r2long)

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

finder=d.find_thx_epci("CC du Rouillacais", df)

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
