from re import template
from flask import Flask,request, url_for, render_template
from Database import database
from Regression import regression
from Mapping import mapping
import pandas as pd
import folium

app = Flask(__name__,template_folder='templates')
df=pd.read_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\PPE\PPE\regression.csv')
d=database('C:/Users/lilia/OneDrive/Documents/Lilian/ING4_S2/PPE/PPE/Clean2gether.json')

epci_data=d.all_epci(df)
county_data=d.all_county(df)
r=regression(df)
mlrlat,mlrlong,rmselat,rmselong,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat,y_testlat,y_testlong=r.opti_regression()
mlr_weight,r2,rmse=r.weight_regression()

@app.route('/')  
def home ():  
    return render_template("home.html")  

@app.route('/index', methods=["GET","POST"])
def scdPage():
   if request.method == "POST":

      variable1 = request.form.get("variable1")
      variable2 = request.form.get("variable2")
      variable3 = request.form.get("variable3")

      if (variable1 =="EPCI"):

         finder=d.find_thx_epci(variable2, df)
         pred_lat=mlrlat.predict(finder)
         pred_long=mlrlong.predict(finder)
         coord=pd.DataFrame(columns=["latitude","longitude"])
         coord["latitude"]=pred_lat
         coord["longitude"]=pred_long
         weight=pd.DataFrame(mlr_weight.predict(coord),columns=["weight"])
         m=mapping(pred_long,pred_lat)
         c=m.create_map_prediction(weight)
         
         return c._repr_html_()

      elif (variable1 =="County"):

         finder=d.find_thx_county(variable3, df)
         pred_lat=mlrlat.predict(finder)
         pred_long=mlrlong.predict(finder)
         coord=pd.DataFrame(columns=["latitude","longitude"])
         coord["latitude"]=pred_lat
         coord["longitude"]=pred_long
         weight=pd.DataFrame(mlr_weight.predict(coord),columns=["weight"])
         m=mapping(pred_long,pred_lat)
         c=m.create_map_prediction(weight)

         return c._repr_html_()

      else :

         c = folium.Map()
         return c._repr_html_()

   else :
      return render_template('index.html')

if __name__ == '__main__':
   app.run()(debug = True) 