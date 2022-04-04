from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import time

class regression:

        def __init__(self, data_base):
                self.data_base = data_base
                
        def long_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["postcode","total_weight","epci_weight","postcode_weight","town_weight","county_weight","num_county","num_epci","num_town"]]
            y = data_base["longitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = None)

            mlr = LinearRegression()  
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)

            return mlr,r2,rmse,y_pred_mlr,y_train,x_test

        def lat_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["postcode","total_weight","epci_weight","postcode_weight","town_weight","county_weight","num_county","num_epci","num_town"]]
            y = data_base["latitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = None)

            mlr = LinearRegression()  
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)

            return mlr,r2,rmse,y_pred_mlr,y_train

        def opti_regression(self):

            start_time = time.time()
            
            mlr=pd.DataFrame(columns=["mlr_lat","mlr_long",'r2_lat','r2_long'])
            
            for i in range(500):
                mlrlat,r2lat,rmselat,y_pred_mlrlat,y_trainlat=self.lat_reg()
                mlrlong,r2long,rmselong,y_pred_mlrlong,y_trainlong,x_test=self.long_reg()
                mlr=mlr.append({"mlr_lat" :mlrlat ,"mlr_long" : mlrlong, 'r2_lat' :float(r2lat), 'r2_long' :float(r2long) } , ignore_index=True)
            
            best_mlr_lat = mlr['mlr_lat'][mlr["r2_lat"].idxmax()]
            best_mlr_long = mlr['mlr_long'][mlr["r2_long"].idxmax()]
            best_r2lat = mlr['r2_lat'][mlr["r2_lat"].idxmax()]
            best_r2long = mlr['r2_long'][mlr["r2_long"].idxmax()]
            
            interval = time.time() - start_time
            
            print(interval)
            
            return best_mlr_lat,best_mlr_long,best_r2lat,best_r2long,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat

