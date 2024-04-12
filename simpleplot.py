"""
A simple Plotly display, which shows that both width and height are responsive
to viewport size when a figure is not wrapped in a Dasg Graph object
"""
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# data
df = px.data.gapminder()
df["lifeExp"] = df["lifeExp"].round(1)
df["GDP per person"] = df["gdpPercap"].round(0)
df["Pop (m)"] = (df["pop"]/1000000.).round(1)
df = df.drop(columns=["gdpPercap","pop","iso_num"]).rename(columns={"iso_alpha":"iso"})
g7 = {"CAN","FRA","DEU","ITA","JPN","GBR","USA"}
df7 = df[df["iso"].isin(g7)]

fig = px.line(df7, x="year", y="GDP per person", color="country", markers=True,
             title="GDP per person for G7 countries")
fig.update_layout(dragmode="pan", showlegend=False, 
                  margin={"l":40,"t":50,"r":0,"b":20},
                  #height=300,
                  autosize=True,
                  )

if __name__ == '__main__':
    fig.show()
