# app
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
            dbc.NavItem(dbc.NavItem(dbc.NavLink("Analysis", href="/Analysis"))),
            dbc.DropdownMenu(
                children= [
                    dbc.DropdownMenuItem("Raw Data", href="/RawData"),
                    dbc.DropdownMenuItem("Truck Data", href="/TruckData"),
                    dbc.DropdownMenuItem("Exceptions Graph", href="/ExceptionsGraph"),
                    ],
                nav=True,
                in_navbar=True,
                label="Data",),
        ],
    brand="Balea Data Analysis",
    brand_href="/",
    color="primary",
    dark=True)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("Home page")
    elif pathname == "/RawData":
        return html.Div(dash_table.DataTable(id = 'table-head',columns = [{"name":i, "id":i} for i in df.columns],data = df.to_dict('records'),page_size=50))
    elif pathname == "/TruckData":
        return html.Div( dash_table.DataTable(id = 'new-table',columns = [{"name":i, "id":i} for i in newDF.columns],data = newDF.to_dict('records')))
    elif pathname == "/ExceptionsGraph":
        return html.Div(dcc.Graph(id='graph-of-new-data',figure=fig))
    elif pathname == "/Analysis":
        return html.Div(dcc.Graph(id='data-graph',figure=fig2))
    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url") ,
    
    navbar,
    content

    
])

if __name__ == '__main__':
    app.run_server(debug=True)