import pandas as pd
import numpy as np

class database(object):
     def __init__(self, url):
                self.url = url

     def create_data(self):
        data =pd.read_csv(self.url)
        del data["SIGNALEMENT"]
        del data["EMPLACEMENT"]
        del data["PRENOM"]
        del data["MAIL"]

        data = data.dropna()

        data = data.astype({"VILLE":"int","Quartier":"int", "TYPE": "int"})
        #quartierDf = pd.DataFrame(columns=['Name','Weight'])
        #for quartier in data["Quartier"]:
        #    temp = False
        #    for index in quartierDf.index:
        #        if quartier == quartierDf['Name'][index]:
        #            temp = True
        #            quartierDf['Weight'][index] = quartierDf['Weight'][index] + 1
        #    if temp == False:
        #        quartierDf.loc[len(quartierDf)] = [quartier, 1]

        print(data)

        return data




