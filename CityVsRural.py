from VisualizationData import VisualizationData
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from CountyPoliticalGradRate import fig_2
import pandas as pd
import json


data_object = VisualizationData(3)
dfs = []
# Dictionary for every subgroup we will include in our visualization
subgroups = {'All':1,'Female':2,'Male':3,'American Indian or Alaskian Native':4,\
    'Black or African American':5,'Hispanic or Latino':6,\
    'Asian or Native Hawaiian/Other Pacific Islander':7,\
    'White':8, 'Multiracial':9,'General Education Students':10,\
    'Students with Disabilities':11,'English Language Learner':13,\
    'Economically Disadvantaged':15, 'Migrant':17,'Homeless':20, \
    'In Foster Care':22
    }


# Dictionary for looking up dataframes
dataframes = {}
for subgroup_name,subgroup_category in subgroups.items():
    dataframes[subgroup_name] = data_object.df.loc[data_object.df['subgroup_code']==subgroup_category]
    # uncomment either of these lines to "fake" clicking on a county.
    
    # First county - a republican county. Just replace 'St.Lawrence' with a different county name if you want to show
    # its data
    #dataframes[subgroup_name] = dataframes[subgroup_name].loc[data_object.df['COUNTY']=='St.Lawrence'] 
    
    # Second county - a democractic (city) county. Same as above - replace 'Suffolk' with a different county name
    # if you want to show only its data.
    #dataframes[subgroup_name] = dataframes[subgroup_name].loc[data_object.df['COUNTY']=='Suffolk'] 

# Create figure
fig = make_subplots(rows=1,cols=2,specs=[[{"type":"mapbox"},{"type":"scatter"}]],subplot_titles=[
    "New York County Map and Political Affiliation","Dropout rate by Needs to Resource Category"
])
    # Each scatterplot technically is 3 traces.
    # We create these three traces at once, and then add them to the list.
    # Then, when we create the buttons, they update 3 traces at once.

# Create traces
for subgroup_name, df in dataframes.items(): 
    df_one = df.loc[df['location category']=='NYC']
    trace1 = go.Scatter(
                x= df_one['enroll_cnt'],
                y= df_one['dropout_pct'],
                text = df_one['aggregation_name'],
                name = 'NYC',
                mode = 'markers',
                customdata=df_one['COUNTY'],
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}%<br>" +
                "County: %{customdata}"
                )
    df_two = df.loc[df['location category']=='Buffalo, Rochester, Yonkers, or Syracuse'] 
    trace2 = go.Scatter(
                x= df_two['enroll_cnt'],
                y= df_two['dropout_pct'],
                text = df_two['aggregation_name'],
                name = 'Buffalo, Rochester, Yonkers, or Syracuse',
                mode = 'markers',
                customdata=df_two['COUNTY'],
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}%<br>" +
                "County: %{customdata}"
                )
    df_three = df.loc[df['location category']=='Non-major city school']
    trace3 = go.Scatter(
                x= df_three['enroll_cnt'],
                y= df_three['dropout_pct'],
                text = df_three['aggregation_name'],
                name = 'Other Category',
                mode = 'markers',
                customdata=df_three['COUNTY'],
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}%<br>" +
                "County: %{customdata}"
                )
    fig.add_trace(trace1,row=1,col=2)
    fig.add_trace(trace2,row=1,col=2)
    fig.add_trace(trace3,row=1,col=2)

fig.add_trace(fig_2(),row=1,col=1)
# Show only first 3 traces
# Figures 0, 1 and 2 are what we want so we start at 3
for i in range(3,len(subgroups)*3):
    fig.update_traces(visible=False,selector = i,row = 1, col = 2)

# Add buttons
# Function for this
def create_layout_button(k, subgroup_name):
        visibility= [False]*3*len(subgroups) # We have 3 * len(subgroup) items
        visibility.append(True) # Last item is our map
        for tr in range(3*k, 3*k+3):
            visibility[tr] =True
        return dict(label = subgroup_name,
                    method = 'restyle',
                    args = [{'visible': visibility,
                             'title': subgroup_name,
                             'showlegend': True}])

button_list = []
i = 0
for subgroup_name,value in subgroups.items():
    button_list.append(create_layout_button(i,subgroup_name))
    i+=1
    
fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = button_list
            )
        ])
fig.update_layout(
    height=800,
    title_text='<b>New York State County Political Affiliation vs High School Dropout Data</b>'+
    "<br>Does the population and political affiliation of a school's county affect its graduation rate?</sup><br><br>",
    xaxis_title="Number of Students",
    yaxis_title="Dropout Rate (percent)",
    legend_title = "Need to Resource Capacity Category",
    title_x = 0.5,
    title_y=0.97
)

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=4.5, mapbox_center = {"lat": 43, "lon": -76})
fig.update_geos(fitbounds="locations",visible=False)
fig.update_traces(showscale=False,row=1,col=1)
        
config = {'displayModeBar': False}

fig.show(config=config)
