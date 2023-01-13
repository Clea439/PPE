from re import template
from flask import Flask,request, url_for, render_template
from SannoisDatabase import database
from PFE_Main import Main
from MappingSannois import mapping
import pandas as pd
import folium

app = Flask(__name__,template_folder='templates')
d=database('sannois_depot_sauvage.csv')

data= Main(d)
prediction, trueValue = data.get_regressions()

@app.route('/')  
def home ():  
    return render_template("home.html")  

@app.route('/index', methods=["GET","POST"])
def scdPage():
   if request.method == "POST":
        m=mapping(prediction, trueValue)
        c=m.create_map_prediction()

        return c._repr_html_()


   else :
            return render_template('index.html')


if __name__ == '__main__':
   app.run()(debug = True) 