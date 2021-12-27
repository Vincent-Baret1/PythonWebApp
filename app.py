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

comboListWeights = []
for i in range(0, len(df)):
    theoWeight = df.WeightProductTradeUnitUsed[i]
    if df.Quantity[i] != 0:
        measuredWeight = df.Weight[i] / df.Quantity[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], 0, df.Weight[i]))
    else:
        measuredWeight = df.Weight[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], 0, df.Weight[i]))


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

ratWeight = []
negWeight = []
for truck in listOfTrucks:
    cnt = 0
    totalWeightDiv = 0
    cntNegWeight = 0
    for name, rat, wgt in comboListWeights:
        if truck == name:
            cnt += 1
            totalWeightDiv += rat
            if wgt <= 0:
                cntNegWeight += 1
    ratWeight.append(totalWeightDiv / cnt)
    negWeight.append(cntNegWeight)

zipped = list(zip(listOfTrucks, countTarExceptions, missionsOfTruck, exceptionRate, flagTARCorrelation, ratWeight, negWeight))
newDF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumMissions', 'ExceptionRate', 'TARCorrelation', 'AvgWeightDiff', 'NumNegativeWeights'])

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
