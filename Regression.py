from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class regression:

        def __init__(self, data_base):
                self.data_base = data_base
                
        def long_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["weight","postcode","epci","town","county"]]
            y = data_base["longitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = None)

            mlr = LinearRegression()  
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)

            return mlr,r2,rmse,y_pred_mlr,y_train

        def lat_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["weight","postcode","epci","town","county"]]
            y = data_base["latitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = None)

            mlr = LinearRegression()  
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)

            return mlr,r2,rmse,y_pred_mlr,y_train


