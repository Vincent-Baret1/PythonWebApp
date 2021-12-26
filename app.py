# app
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

df = pd.read_csv('data_balea.csv', sep=';')

comboListTAR = []
for i in range(0, len(df)):
    comboListTAR.append((df.TruckName[i], df.TARException[i]))

comboListFlag = []
for i in range(0, len(df)):
    comboListFlag.append((df.TruckName[i], df.TARException[i], df.FlagWeightOverriden[i]))

listOfTrucks = []
for truck in df.TruckName:
    if truck not in listOfTrucks:
        listOfTrucks.append(truck)

countTarExceptions = []
for truck in listOfTrucks:
    count = 0
    for name,exp in comboListTAR:
        if name == truck:
            if exp == 1:
                count += 1
    countTarExceptions.append(count)

missionsOfTruck = []
for truck in listOfTrucks:
    count = 0
    for name,cnt in comboListTAR:
        if name == truck:
            count += 1
    missionsOfTruck.append(count)

exceptionRate = []
for i in range(0, len(countTarExceptions)):
    exceptionRate.append(countTarExceptions[i]/missionsOfTruck[i])

flagTARCorrelation = []
for truck in listOfTrucks:
    countEquals = 0
    countTotal = 0
    for name, e, f in comboListFlag:
        if truck == name:
            countTotal += 1
            if e == f:
                countEquals += 1
    flagTARCorrelation.append(countEquals/countTotal)


zipped = list(zip(listOfTrucks, countTarExceptions, missionsOfTruck, exceptionRate, flagTARCorrelation))
newDF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumMissions', 'ExceptionRate', 'TARCorrelation'])

dfHead = df.head()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Balea Data Analysis'),

    html.Div(children='''
        Header table of the raw data.
    '''),

    dash_table.DataTable(
    id = 'table-head',
    columns = [{"name":i, "id":i} for i in dfHead.columns],
    data = dfHead.to_dict('records'),
    ),

    html.Div(children='''
        Synthesised table of data for each truck.
    '''),

    dash_table.DataTable(
    id = 'new-table',
    columns = [{"name":i, "id":i} for i in newDF.columns],
    data = newDF.to_dict('records'),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
