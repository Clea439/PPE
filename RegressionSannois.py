from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import time
import numpy as np

class RegressionSannois(object):
    def __init__(self, data_base):
         self.data_base = data_base
    def long_reg(self):
        data_base=self.data_base.dropna()
        x = data_base[["VILLE"]]
        y = data_base["Longitude"]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

        mlr =HistGradientBoostingRegressor()
        mlr.fit(x_train, y_train)

        y_pred_mlr=mlr.predict(x_test)

        r2 = r2_score(y_test, y_pred_mlr)
        rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)
            
        return mlr,r2,rmse,y_pred_mlr,y_train,y_test

    def lat_reg(self):
        data_base=self.data_base.dropna()
        x = data_base[["VILLE"]]
        y = data_base["Latitude"]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

        mlr = HistGradientBoostingRegressor()
        mlr.fit(x_train, y_train)

        y_pred_mlr=mlr.predict(x_test)

        r2 = r2_score(y_test, y_pred_mlr)
        rmse = mean_squared_error(y_test, y_pred_mlr, squared=True)

        return mlr,r2,rmse,y_pred_mlr,y_train,y_test

    def tonnage(self, prediction):
            data_base=self.data_base.dropna()
            x = data_base[["VILLE"]]
            y = data_base["tonnage"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

            mlr = HistGradientBoostingRegressor()
            mlr.fit(x_train, y_train)

            weight=mlr.predict(x_test)

            r2 = r2_score(y_test, weight)
            rmse = mean_squared_error(y_test, weight, squared=False)
            
            return weight, y_train, y_test,r2,rmse

    def type(self):
            data_base=self.data_base.dropna()
            x = data_base[["VILLE"]]
            y = data_base["TYPE"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

            mlr = RandomForestClassifier(random_state=2)
            mlr.fit(x_train, y_train)

            type=mlr.predict(x_test)

            AccuracyScore = accuracy_score(y_test, type)
            
            return type, y_train, y_test, AccuracyScore

    def price(self, prediction):
        data_base=self.data_base.dropna()
        x = data_base[["VILLE"]]
        y = data_base["Tarif"]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

        mlr = HistGradientBoostingRegressor()
        mlr.fit(x_train, y_train)

        tarif=mlr.predict(x_test)

        r2 = r2_score(y_test, tarif)
        rmse = mean_squared_error(y_test, tarif, squared=False)
            
        return tarif,y_train,r2,rmse

    def opti_regression(self):

        start_time = time.time()
            
        mlr=pd.DataFrame(columns=["mlr_lat","mlr_long",'r2_lat','r2_long'])
            
        for i in range(1):
            mlrlat,r2lat,rmselat,y_pred_mlrlat,y_trainlat,y_testlat=self.lat_reg()
            mlrlong,r2long,rmselong,y_pred_mlrlong,y_trainlong,y_testlong=self.long_reg()
            mlr=mlr.append({"mlr_lat" :mlrlat ,"mlr_long" : mlrlong, 'r2_lat' :float(r2lat), 'r2_long' :float(r2long), 'rmselat' :float(rmselat), 'rmselong' :float(rmselong) } , ignore_index=True)
            
        best_mlr_lat = mlr['mlr_lat'][mlr["r2_lat"].idxmax()]
        best_mlr_long = mlr['mlr_long'][mlr["r2_long"].idxmax()]
        r2lat = mlr['r2_lat'][mlr["r2_lat"].idxmax()]
        r2long = mlr['r2_long'][mlr["r2_long"].idxmax()]
        
        interval = time.time() - start_time
            
        print("loading time : "+str(interval)+" sec !" )
            
        return best_mlr_lat,best_mlr_long,r2lat,r2long,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat,y_testlat,y_testlong



