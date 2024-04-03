# From https://dash.plotly.com/tutorial
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
import gunicorn                         # for Heroku

# data
df = px.data.gapminder()
df["lifeExp"] = df["lifeExp"].round(1)
df["GDP per person"] = df["gdpPercap"].round(0)
df["Pop (m)"] = (df["pop"]/1000000.).round(1)
df = df.drop(columns=["gdpPercap","pop","iso_num"]).rename(columns={"iso_alpha":"iso"})
g7 = {"CAN","FRA","DEU","ITA","JPN","GBR","USA"}
df7 = df[df["iso"].isin(g7)]

df["g7"] = ""
df["g7"] = df["g7"].where(~df["iso"].isin(g7),"G7")

# app and layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server                     # for Heroku

columnDefs = [{'field':"country"}, {'field':"year"}] + \
        [ {'field':col} for col in df.columns if col not in {"country", "year"}]
grid = dag.AgGrid(
    rowData=df.to_dict("records"),
    columnDefs=columnDefs,
    defaultColDef={"filter": True},
    columnSize="autoSize",
    dashGridOptions = {"suppressColumnVirtualisation": True, "rowHeight": 26},
    style={"margin-left":"40px","max-height":"80vh"},
)

fig = px.line(df7, x="year", y="GDP per person", color="country", markers=True,
             title="GDP per person for G7 countries")
fig.update_layout(dragmode="pan", showlegend=False, 
                  margin={"l":40,"t":50,"r":0,"b":0}
                  )
#fig.update_yaxes(fixedrange=True)

app.layout = dbc.Container([
    html.H3('Example Graph'),
    dbc.Row([
            dbc.Col(dcc.Graph(
                figure=fig,
                config={'scrollZoom': True,'displayModeBar': False},
            ), lg=6, ),
            dbc.Col(grid, lg=6),
    ]), 
])

if __name__ == '__main__':
    app.run(debug=False)
