import pandas as pd
import numpy as np

class database():

        def __init__(self, url):
                self.url = url
                self.data_fichier=pd.read_json(url)

        def create_data(self):

            df=self.data_fichier[:]

            county = pd.DataFrame(df.pivot_table(index = ['county'], aggfunc ='size') , columns=["nb"])
            town = pd.DataFrame(df.pivot_table(index = ['town'], aggfunc ='size') , columns=["nb"])
            epci = pd.DataFrame(df.pivot_table(index = ['epci'], aggfunc ='size'), columns=["nb"])  
            postcode=pd.DataFrame(df.pivot_table(index = ['postcode'], aggfunc ='size'), columns=["nb"])

            county["num_county"]=np.arange(1,len(county)+1)
            epci["num_epci"]=np.arange(1,len(epci)+1)
            town["num_town"]=np.arange(1,len(town)+1)

            county["weight"]=county["nb"]/len(county)
            town["weight"]=town["nb"]/len(town)
            epci["weight"]=epci["nb"]/len(epci)
            postcode["weight"]=town["nb"]/len(postcode)

            county["county"]=county.index
            town["town"]=town.index
            epci["epci"]=epci.index
            postcode["postcode"]=postcode.index

            df["total_weight"]=np.zeros(len(df))
            df["epci_weight"]=np.zeros(len(df))
            df["postcode_weight"]=np.zeros(len(df))
            df["town_weight"]=np.zeros(len(df))
            df["county_weight"]=np.zeros(len(df))

            for index, row in df.iterrows():
                for index2, row2 in county.iterrows():
                    if row["county"]==row2["county"]:
                        df["total_weight"][index]=row["weight"]+row2["weight"]
                        df["county_weight"][index]=row["weight"]+row2["weight"]
                        df["county"][index]=row2["num_county"]
            
            for index, row in df.iterrows():
                for index2, row2 in postcode.iterrows():
                    if row["postcode"]==row2["postcode"]:
                        df["total_weight"][index]=row["weight"]+row2["weight"]
                        df["postcode_weight"][index]=row["weight"]+row2["weight"]

            for index, row in df.iterrows():
                for index2, row2 in town.iterrows():
                    if row["town"]==row2["town"]:
                        df["total_weight"][index]=row["weight"]+row2["weight"]
                        df["town_weight"][index]=row["weight"]+row2["weight"]
                        df["town"][index]=row2["num_town"]

            for index, row in df.iterrows():
                for index2, row2 in epci.iterrows():
                    if row["epci"]==row2["epci"]:
                        df["total_weight"][index]=row["weight"]+row2["weight"]
                        df["epci_weight"][index]=row["weight"]+row2["weight"]
                        df["epci"][index]=row2["num_epci"]

            del df['images']

            df.to_csv (r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\Untitled Folder\regression.csv', index = False, header=True)
            
            self.data_fichier=df

            return df

        def add_data(self, new_line):
            df=self.data_fichier[:]

            postcode=new_line["postcode"]
            epci=new_line["epci"]
            county=new_line["county"]

    
            county = pd.DataFrame(df.pivot_table(index = ['county'], aggfunc ='size') , columns=["nb"])
            town = pd.DataFrame(df.pivot_table(index = ['town'], aggfunc ='size') , columns=["nb"])
            epci = pd.DataFrame(df.pivot_table(index = ['epci'], aggfunc ='size'), columns=["nb"])  
            df=pd.concat([df,new_line], ignore_index=True)
            return df

