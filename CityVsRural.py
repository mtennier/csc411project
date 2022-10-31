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

subgroup_category = 1
#print(dataframes)
df_one = data_object.df.loc[data_object.df['subgroup_code']==subgroup_category]
#print(df_one)


# Create a bunch of figures

#fig = go.Figure()

""" fig = px.scatter(df_one, x="enroll_cnt", y="dropout_pct", color="location category",
                hover_data=['aggregation_name']) """

traces = []
buttons = []
i = 0
for subgroup_name, df in dataframes.items(): 
    visible = [False] * len(dataframes)
    visible[i] = True
    traces.append(px.scatter(df, x="enroll_cnt", y="dropout_pct", color="location category",
                hover_data=['aggregation_name']).update_traces(visible = True if i==0 else False).data[0])
    buttons.append(dict(label=subgroup_name,
                        method="update",
                        args=[{"visible":visible},
                              {"title":f"{subgroup_name}"}]))

    i+=1
updatemenus = [{'active':0, "buttons":buttons}]
fig = go.Figure(data=traces,
                 layout=dict(updatemenus=updatemenus))
fig.show()