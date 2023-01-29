from re import template
from flask import Flask,request, url_for, render_template
from SannoisDatabase import database
from PFE_Main import Main
from MappingSannois import mapping
import pandas as pd
import folium

app = Flask(__name__,template_folder='templates')
d=database('sannois_depot_sauvage.csv')
travaux =pd.read_csv('Liste-travaux.csv')
travaux = travaux.dropna()

data= Main(d, travaux)
prediction, trueValue = data.get_regressions()
dechetteries =pd.read_csv('DECHETTERIE.csv')
dechetteries = dechetteries.dropna()

m=mapping(prediction, trueValue, dechetteries, travaux)

@app.route('/')  
def home ():  
    return render_template("home.html")  

@app.route('/index', methods=["GET","POST"])
def scdPage():
   if request.method == "POST":
        c=m.create_map_prediction()

        return c._repr_html_()


   else :
            return render_template('index.html')

@app.route('/index/<id>', methods=["GET","POST"])
def setTrue(id):
    prediction.at[int(id),'Verification'] = 1
    c = m.validation_dechet(prediction)
    return c._repr_html_()


if __name__ == '__main__':
    app.run()(debug = True) 