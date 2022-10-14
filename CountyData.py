import pandas as pd
#  remember source .venv/bin/activate     
""" 
    Functon for getting the voter county data.
    Retrieves the data from the CSV, converts it to a
    pandas data frame, parses it & removes redundant information,
    then returns the frame.
"""
def getCountyData()->pd.DataFrame:
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

""" Thought more readable instead of using lambda 
    Determines whethers there's more registered democrats (returns DEM)
    or more registered republicans (returns REP)
    Else, returns EQ
"""
def determineParty(dem_count,rep_count)->str:
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
    

""" 
    getCountyVoterCategoryData
    Using the parsed data, determines the voter category for the county
    based on total registered demoocrats and republicans.
    ie if a county has more democrats than republicans, it is labelled as
    republican
 """
def getCountyVoterCategoryData()->pd.DataFrame:
    original_df = getCountyData() # Get the old data frame
    print(original_df)
    new_df = original_df.filter(['COUNTY'],axis = 1) # Copy over the coounty axi
    new_df['PARTY'] = original_df.apply(lambda x: determineParty(dem_count=x['DEM'],rep_count=x['REP']),axis = 1)
    new_df['RATIO'] = original_df.apply(lambda x: determinePercentage(dem_count=x['DEM'],rep_count=x['REP']),axis = 1)
    print(new_df)

getCountyVoterCategoryData() # Call for testing
