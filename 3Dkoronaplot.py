import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date
from IPython.display import display

while True:
    try:
        df = pd.read_excel("https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"+ str(date.today())[:8] + str(int(str(date.today())[8:])-1) + ".xlsx")
        break
    except:
        print("Error fetching data")
        
while True:
    try:
        days = int(input("Enter observation window (e.g. 20): "))
        break
    except ValueError:
        print("Incorrect input.")
        continue

print("Available countries: " +str(list(pd.unique(df["countriesAndTerritories"]))))

def listcountries():
    countrylist = []
    while True:
        try:
            country = input('\nEnter a country, to start visualization enter "GO": ')
            if country in list(pd.unique(df["countriesAndTerritories"])):
                print("Correct input")
                countrylist.append(country)
            elif country == "GO":
                return(countrylist)
                break   
            else:
                print("Incorrect input.")
                continue
        except ValueError:
            print("Incorrect input.")
            continue
    
def preprocess(df):

    dflist = []
    for country in countrylist:
        dfcountry = df[["dateRep","cases", "deaths", "popData2018"]][df["countriesAndTerritories"] == country]
        dfcountry['country'] = country
        dfcountry = dfcountry.iloc[::-1]
        dfcountry["cumCases"] = dfcountry["cases"].cumsum(axis = 0, skipna = True)
        dfcountry["cumDeaths"] = dfcountry["deaths"].cumsum(axis = 0, skipna = True)
        dflist.append(dfcountry)
    dfTemporal = pd.concat(dflist)
    dfTemporal["dateRep"] = dfTemporal["dateRep"].astype("str")
    return(dfTemporal)


def lineplotCaseDeath(df, countrylist, days):
    
    fig = px.line_3d(df, x="dateRep", y="popData2018", z="cumCases", color='country', title="Cases")
    fig.show()

    fig = px.line_3d(df, x="dateRep", y="popData2018", z="cumCases", color='country', title="Deaths")
    fig.show()

countrylist = listcountries()
df = preprocess(df)
lineplotCaseDeath(df, countrylist, int(days))