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
    new_drop = ['aggregation_type', 'aggregation_code',
       'aggregation_name','nrc_code', 'nrc_desc','nyc_ind', 
       'membership_key', 'membership_desc']
    new_df = old_df.drop(new_drop,axis=1)
    new_df = new_df.loc[new_df['aggregation_index']==2] # Aggregation column for counties
    new_df.drop('aggregation_index',axis=1,inplace=True) # Drop aggregation column, not needed
    new_df['county_name']=new_df.apply(lambda x: x['county_name'].capitalize(),axis=1) # Change formatting of county names 
    new_df.loc[new_df['county_name'] == 'Saint lawrence','county_name'] = 'St.Lawrence' # wont merge properly if we dont do this
    new_df.loc[new_df['membership_code'] ==9] # Only get 4 year cohorts
    optional_drop_categories = ['membership_code','grad_cnt','grad_pct',
    'local_cnt','local_pct','reg_cnt','reg_pct','reg_adv_cnt','reg_adv_pct','non_diploma_credential_cnt',
    'non_diploma_credential_pct','still_enr_cnt','still_enr_pct','ged_cnt','ged_pct','dropout_cnt']

    new_df['dropout_pct'] = old_df['dropout_pct'].str.strip('%')
    new_df.drop(new_df.loc[new_df['dropout_pct']=='-'].index, inplace=True)
    new_df[['dropout_pct']] = new_df[['dropout_pct']].apply(pd.to_numeric)
    new_df.drop(optional_drop_categories,axis=1,inplace=True)
    return new_df

def resourceAllocationCategory(c:int)->str:
    """ 
        Helper function for getSchoolData2.
        Takes in a integer representing an NRC category
        and then generalizes the category based on that.
        We need this since we kinda generalize the category data for the plot.
     """
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
    drop_categories = ['aggregation_index','aggregation_type','aggregation_code','nrc_desc','nyc_ind']
    new_df.drop(drop_categories,axis=1,inplace=True)
    new_df['location category'] = new_df.apply(lambda x: resourceAllocationCategory(c= x['nrc_code']),axis=1)
    new_df = new_df.loc[new_df['membership_code'] ==9] # Only get 4 year cohorts
    optional_drop_categories = ['nrc_code','membership_code','membership_desc','grad_cnt','grad_pct',
    'local_cnt','local_pct','reg_cnt','reg_pct','reg_adv_cnt','reg_adv_pct','non_diploma_credential_cnt',
    'non_diploma_credential_pct','still_enr_cnt','still_enr_pct','ged_cnt','ged_pct','dropout_cnt']
    new_df.drop(optional_drop_categories,axis=1,inplace=True)
    new_df['dropout_pct'] = old_df['dropout_pct'].str.strip('%')
    new_df.drop(new_df.loc[new_df['dropout_pct']=='-'].index, inplace=True)
    new_df[['dropout_pct']] = new_df[['dropout_pct']].apply(pd.to_numeric)
    new_df['county_name']=new_df.apply(lambda x: x['county_name'].capitalize(),axis=1) # Change formatting of county names
    new_df.loc[new_df['county_name'] == 'Saint lawrence','county_name'] = 'St.Lawrence'
    new_df.loc[new_df['county_name'] == 'New york','county_name'] = 'New York'
    #print(new_df) #for testing
    return new_df

getSchoolData2()