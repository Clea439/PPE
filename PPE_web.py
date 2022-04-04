from Database import database
from Regression import regression
from Mapping import mapping
import pandas as pd

df=pd.read_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\Untitled Folder\regression.csv')
d=database('C:/Users/lilia/OneDrive/Documents/Lilian/ING4_S2/Untitled Folder/Clean2gether.json')

r=regression(df)

mlrlat,r2lat,rmselat,y_pred_mlrlat,y_trainlat=r.lat_reg()
mlrlong,r2long,rmselong,y_pred_mlrlong,y_trainlong,x_test=r.long_reg()

print(r2lat)
print(r2long)
print(rmselat)
print(rmselong)

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
