from urllib.request import urlopen
import json
from VisualizationData import VisualizationData
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
def fig_2():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = make_subplots(
    rows=1, cols=2, subplot_titles=('Map1', 'Map2'),
    specs=[[{"type": "mapbox"}, {"type": "mapbox"}]])
    data_object = VisualizationData(1)
    df = data_object.df
    # uncomment this line to only show a county (for the fake visualization)
    # this code is assuming you are clicking on 'Academy School.' Note:
    # I am simply filtering the dataframe so it only has data for the county belonging to the
    # school clicked on so if you want to click a different point, just hover over it to find
    # its county, and then replace 'Erie' with the school's county
    #df = df.loc[df['COUNTY']=='Erie'] 
    
    fig.add_trace(go.Choroplethmapbox(geojson=counties, 
                                  locations=df.FIPS, 
                                  z=df.PARTYNUM, zmin = 0, zmax = 1,
                                  colorscale = [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']],
                                  text = df['COUNTY'],
                                  hovertemplate='County Name: %{text}',
                                  marker_line_color='white',
                                  showlegend=False
                                  ),row=1,col=1)
    # add this to final
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 43, "lon": -76})
    fig.update_geos(fitbounds="locations",visible=False)
    fig.update_traces(showscale=False)
    #fig.show()
    return go.Choroplethmapbox(geojson=counties, 
                                    locations=df.FIPS, 
                                    z=df.PARTYNUM, zmin = 0, zmax = 1,
                                    colorscale = [[0, 'rgb(255,0,0)'], [1, 'rgb(0,0,255)']],
                                    text = df['COUNTY'],
                                    customdata = df['PARTY'],
                                    hovertemplate='<b>County Name: %{text}</b><br><br>'+
                                    "Political party: %{customdata}",
                                    showlegend=False,
                                    marker_line_color='white'
                                    )