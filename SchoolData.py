import pandas as pd
from CountyData import *
"""
    Set of functions for retrieving and parsing the 
    NY State Grad Rate data.
"""
def initialParseSchoolData() -> pd.DataFrame:
    """ 
        Does initial parsing of the school data.
        Parses everything we don't need for all versions of
        the school data.
        Returns a dataframe containing the parsed data.
     """
    df = pd.read_csv('GRAD_RATE_AND_OUTCOMES_2021.csv')
    # Begin dropping unneccesary columns
    drop_columns = ['report_school_year','lea_beds','lea_name','boces_code','boces_name','county_code']
    # There's way too many rows to just drop unncessary - we shall index them as needed
    df.drop(drop_columns,axis=1,inplace=True)
    #print(df)
    #print(df.columns)
    return df

def getSchoolData1() -> pd.DataFrame:
    """ 
        Parses the school data for Visualization 1 - the map.
        Removes all unneeded columns and grabs the aggregations we need.
        Returns a dataframe containing the finalized needed school data for
        visualization 1.
    """
    old_df = initialParseSchoolData()
    # Get all data for counties
    new_drop = ['aggregation_type', 'aggregation_code',
       'aggregation_name','nrc_code', 'nrc_desc','nyc_ind',
       'membership_code', 'membership_key', 'membership_desc', 'subgroup_code',
       'subgroup_name']
    new_df = old_df.drop(new_drop,axis=1)
    new_df = new_df.loc[new_df['aggregation_index']==2] # Aggregation column for counties
    new_df.drop('aggregation_index',axis=1,inplace=True) # Drop aggregation column, not needed
    new_df['county_name']=new_df.apply(lambda x: x['county_name'].capitalize(),axis=1)
    # Change formatting of county names
    #print(new_df)
    return new_df

def resourceAllocationCategory(c:int)->str:
    category = ''
    if c == 1:
        category = 'NYC'
    elif c ==  2:
        category = 'Buffalo, Rochester, Yonkers, or Syracuse'
    else:
        category = 'Non-major city school'
    return category

def getSchoolData2() -> pd.DataFrame:
    """ 
        Parses the school data for Visualization 2 - the scatterplot.
        Removes all unneeded columns and grabs the aggregations we need.
        Returns a dataframe containing the finalized needed school data for
        visualization 2.
    """
    old_df = initialParseSchoolData()
    #print(old_df)
    # Get the aggregation column for school names
    new_df = old_df.loc[old_df['aggregation_index']==4] # Aggregation column for schools
    new_df = new_df.loc[new_df['subgroup_code']==1]
    drop_categories = ['aggregation_index','aggregation_type','aggregation_code','nrc_desc','county_name','nyc_ind']
    new_df.drop(drop_categories,axis=1,inplace=True)
    new_df['location category'] = new_df.apply(lambda x: resourceAllocationCategory(c= x['nrc_code']),axis=1)
    print(new_df) #for testing
    return new_df

def getSchoolData3()-> pd.DataFrame:
    """ 
        Parses the school data for Visualization 3 - the bar graph.
        Removes all unneeded columns and grabs the aggregations we need.
        Returns a dataframe containing the finalized needed school data for
        visualization 3.
    """
    #TODO
    return None



getSchoolData2()