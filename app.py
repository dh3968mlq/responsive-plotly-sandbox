# From https://dash.plotly.com/tutorial
# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = px.data.gapminder()
df["lifeExp"] = df["lifeExp"].round(1)
df["GDP per person"] = df["gdpPercap"].round(0)
df = df.drop(columns="gdpPercap")
g7 = {"CAN","FRA","DEU","ITA","JPN","GBR","USA"}
df7 = df[df["iso_alpha"].isin(g7)]

# Initialize the app
app = Dash(__name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP,
                          #'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css',
])

# App layout
columnDefs = [ {'field':col} for col in df.columns]

grid = dag.AgGrid(
    id="getting-started-filter",
    rowData=df.to_dict("records"),
    columnDefs=columnDefs,
    className="ag-theme-alpine"
)

fig = px.line(df7, x="year", y="GDP per person", color="country", markers=True,
             title="GDP per person for G7 countries")

app.layout = html.Div([
        dbc.Row([
            html.Div('Example Graph', className="text-center fs-3"),
        ]),
        dbc.Row([
            dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                        value='lifeExp',
                        inline=True,
                        id='radio-buttons', className='bg-info rounded-1 my-2')
        ],),
        dbc.Row(
            [
                dbc.Col([
                    grid
                    #dash_table.DataTable(
                    #    data=df.to_dict('records'), 
                    #    page_size=12, 
                        #style_table={'overflowX': 'auto'},
                        #className="dbc",
                    #)
                    ],
                    md=6,
                    id='col-datatable',
                ),
                dbc.Col([
                    #dcc.Graph(figure={}, id='fig-barchart')
                    dcc.Graph(figure=fig),
                    ],
                    id='col-graph',
                    md=6,
                ),
            ],
            className='dbc',
        ), 
    ], className="page-body")

# Add controls to build the interaction
@callback(
    Output('fig-barchart', component_property='figure'),
    Input(component_id='radio-buttons', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
