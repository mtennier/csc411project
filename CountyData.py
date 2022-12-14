import pandas as pd
#  remember source .venv/bin/activate     

def getCountyPoliticalData()->pd.DataFrame:
    """ 
    Functon for getting the voter county data.
    Retrieves the data from the CSV, converts it to a
    pandas data frame, parses it & removes redundant information,
    then returns the frame.
    """
    df = pd.read_csv('county_Feb21.csv',header=4)
    # Drop all NaN rows - this also drops the statewide rows for us
    df.dropna(inplace=True) 
    # These are the active and inactive voter rows - we are just using totals
    activeInactiveRows = df.loc[df['STATUS']=='Active'].index.append(df.loc[df['STATUS']=='Inactive'].index)
    # These are the unneccesary columns - other voting parties, ect
    # We might be able to do something cool with the region so I'm keeping it
    # Same for total 
    dropColumns = ['CON','WOR','OTH','STATUS','BLANK']
    df.drop(activeInactiveRows, inplace=True)
    df.drop(dropColumns,axis=1,inplace=True)
    # Remove all the commas in the numbers
    df = df.apply(lambda x: x.str.replace(',', ''))
    # Cast to proper var types
    df = df.astype({'DEM':int,
                    'REP':int,
                    'TOTAL':int    })
    
    return df


def determineParty(dem_count,rep_count)->str:
    """ Thought more readable instead of using lambda 
    Determines whethers there's more registered democrats (returns DEM)
    or more registered republicans (returns REP)
    Else, returns EQ
    """
    category = ''
    if dem_count > rep_count:
        category = 'DEM'
    elif rep_count > dem_count:
        category = 'REP'
    else:
        category = 'EQ'
    return category

""" Still determining whether to do percentage or ratio.
    Tomorrow project

 """
def determinePercentage(dem_count,rep_count)->float:
    """  percentage = 0.0
    if dem_count > rep_count:
        percentage = dem_count/total_count
    elif rep_count > dem_count:
        percentage = rep_count/total_count
        
    return percentage 
    """
    return dem_count/rep_count

def determinePartyNumber(dem_count,rep_count):
    if dem_count > rep_count:
        return 1
    else:
        return 0

def getCountyVoterCategoryData()->pd.DataFrame:
    """ 
    getCountyVoterCategoryData
    Using the parsed data, determines the voter category for the county
    based on total registered demoocrats and republicans.
    ie if a county has more democrats than republicans, it is labelled as
    republican
    """
    original_df = getCountyPoliticalData() # Get the old data frame
    #print(original_df)
    new_df = original_df.filter(['COUNTY'],axis = 1) # Copy over the coounty axis
    new_df['PARTY'] = original_df.apply(lambda x: determineParty(dem_count=x['DEM'],rep_count=x['REP']),axis = 1)
    new_df['RATIO'] = original_df.apply(lambda x: determinePercentage(dem_count=x['DEM'],rep_count=x['REP']),axis = 1)
    new_df['PARTYNUM'] = original_df.apply(lambda x: determinePartyNumber(dem_count=x['DEM'],rep_count=x['REP']),axis = 1)

    #print(new_df)
    return new_df

def addFipsData()->pd.DataFrame:
    '''
    addFipsData
    Fips codes are needed to us the plotly express map tool.
    This uses another CSV that contains fips codes
    to add them to the county data.
    '''
    old_df = getCountyVoterCategoryData()
    fips_df = pd.read_csv('New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv')
    fips_df.loc[fips_df['County Name'] == 'St. Lawrence', 'County Name'] = 'St.Lawrence'
    to_drop = ['State FIPS','County Code', 'ZIP Code', 'File Date']
    fips_df.drop(to_drop,axis=1,inplace=True)
    fips_df.drop_duplicates(inplace=True)
    old_df['COUNTY'] = old_df['COUNTY'].str.strip() # Discovered this too fucking late. Ugh
    new_df = pd.merge(old_df,fips_df,left_on='COUNTY',right_on='County Name')
    new_df.drop('County Name',axis=1,inplace=True)
    new_df.rename(columns={'County FIPS':'FIPS'},inplace=True)
    return new_df

def getCountyData():
    '''
    getCountyData
    Retrieves the finalized county data.
    Wrapper for readability.
    Returns the finalized county data frame.
    '''
    return addFipsData()