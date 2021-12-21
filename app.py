# app
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

df = pd.read_csv('data_balea.csv', sep=';')
print(df)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id = 'table',
    columns = [{"name":i, "id":i} for i in df.columns],
    data = df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)
