from VisualizationData import VisualizationData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

data_object = VisualizationData(2)
dfs = []
# Dictionary for every subgroup we will include in our visualization
subgroups = {'All':1,'Female':2,'Male':3,'American Indian or Alaskian Native':4,\
    'Black or African American':5,'Hispanic or Latino':6,\
    'Asian or Native Hawaiian/Other Pacific Islander':7,\
    'White':8, 'Multiracial':9,'General Education Students':10,\
    'Students with Disabilities':11,'English Language Learner':13,\
    'Migrant':17,'Homeless':20,'In Foster Care':22
    }


# Dictionary for looking up dataframes
dataframes = {}
for subgroup_name,subgroup_category in subgroups.items():
    dataframes[subgroup_name] = data_object.df.loc[data_object.df['subgroup_code']==subgroup_category]


# Create figure
fig = go.Figure()

""" 
    Each scatterplot technically is 3 traces.
    We create these three traces at once, and then add them to the list.
    Then, when we create the buttons, they update 3 traces at once.
    Clever
"""

# Create traces
for subgroup_name, df in dataframes.items(): 
    df_one = df.loc[df['location category']=='NYC']
    trace1 = go.Scatter(
                x= df_one['enroll_cnt'],
                y= df_one['dropout_pct'],
                text = df_one['aggregation_name'],
                name = 'NYC',
                mode = 'markers',
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}% "
                )
    df_two = df.loc[df['location category']=='Buffalo, Rochester, Yonkers, or Syracuse'] 
    trace2 = go.Scatter(
                x= df_two['enroll_cnt'],
                y= df_two['dropout_pct'],
                text = df_two['aggregation_name'],
                name = 'Buffalo, Rochester, Yonkers, or Syracuse',
                mode = 'markers',
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}% "
                )
    df_three = df.loc[df['location category']=='Non-major city school']
    trace3 = go.Scatter(
                x= df_three['enroll_cnt'],
                y= df_three['dropout_pct'],
                text = df_three['aggregation_name'],
                name = 'Other',
                mode = 'markers',
                hovertemplate = "<b>%{text}</b><br><br>" +
                "Dropout percentage: %{y}% "
                )
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.add_trace(trace3)

# Show only first 3 traces

# Figures 0, 1 and 2 are what we want so we start at 3
for i in range(3,len(subgroups)*3):
    fig.update_traces(visible=False,selector = i)

# Add buttons

# Function for this
def create_layout_button(k, subgroup_name):
        visibility= [False]*3*len(subgroups) # We have 3 * len(subgroup) items
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
    title_text='High School Dropout Rates in New York State ',
    xaxis_title="Number of Students",
    yaxis_title="Dropout Rate (percent)",
    legend_title = "Resource Allocation Category"
)

fig.show()
