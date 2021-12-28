# app
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

print("Reading raw data...")
df = pd.read_csv('data_balea.csv', sep=';')
newDF = pd.read_csv('data_trucks.csv', sep=',')
figDF = pd.read_csv('data_fig.csv', sep=',')
print("Data read.")

list1 = []
list2 = []
list3 = []
for i in range(0, len(newDF)):
    if newDF.ExceptionRate[i] >= 0.06 and newDF.NumMissions[i] >= 1000:
        list1.append(newDF.Trucks[i])
        list2.append(newDF.ExceptionRate[i])
        list3.append(newDF.NumNegativeWeights[i])
zipped = list(zip(list1, list2, list3))
fig2DF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumNegativeWeights'])

# make figure
fig = px.scatter(figDF, x="missions", y="exceptions", color="names", hover_name="names", log_x=True)
fig2 = px.bar(fig2DF, x="Trucks", y="NumNegativeWeights", color="Trucks", hover_name="Trucks")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Balea Data Analysis'),

    dcc.Tabs([
        dcc.Tab(label='Data', children=[
            dcc.Tabs([
                dcc.Tab(label='Raw Data', children=[
                    html.Div(children='''
                        Header table of the raw data.
                    '''),
                    dash_table.DataTable(
                    id = 'table-head',
                    columns = [{"name":i, "id":i} for i in df.columns],
                    data = df.to_dict('records'),
                    page_size=50
                    )
                ]),

                dcc.Tab(label='Truck Data', children=[
                    html.Div(children='''
                        Synthesised table of data for each truck.
                    '''),
                    dash_table.DataTable(
                    id = 'new-table',
                    columns = [{"name":i, "id":i} for i in newDF.columns],
                    data = newDF.to_dict('records')
                    )
                ]),
                
                dcc.Tab(label='Exceptions Graph', children=[
                    dcc.Graph(
                        id='graph-of-new-data',
                        figure=fig
                    )
                ]),
            ])
        ]),
        dcc.Tab(label='Analysis', children=[
            html.H1(children='Balea Truck Data Analysis'),

            dcc.Graph(
                id='data-graph',
                figure=fig2
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
