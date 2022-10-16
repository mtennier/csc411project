import pandas as pd
from CountyData import *
from SchoolData import *
class VisualizationData:
    def VisualizationData(self,option):
        '''
            Creates new object containing all the visualization data needed.
            Option is for choosing which visualization.
            1 = first sketch
            2 = second sketch
            3 = third sketch
            Assumes you arent stupid and won't enter an invalid number
        '''
        if option == 1:
            self.df = getDataFrame1()
        elif option == 2:
            self.df = getDataFrame2()
        else:
            self.df = getDataFrame3()
            
    def getDataFrame1(self) -> pd.DataFrame:
        """ 
            getDataFrame1
            Returns a single dataframe containing all of the data needed
            for the first visualization - county voter association vs dropoutt rate.
            Additional data has also been included, in case more interactivity is to be
            added.  
        """
        county_political_df = getCountyData()
        school_df = getSchoolData1()
        new_df = pd.merge(county_political_df,school_df,left_on = 'COUNTY',right_on = 'county_name')
        new_df.drop('county_name',axis=1,inplace=True)
        return new_df

    def getDataFrame2(self):
        """ 
            getDataFrame2
            Returns a single dataframe containing all of the data needed
            for the second visualization - the scatterplot.
        """
        #TODO
        return None
    def getDataFrame3(self):
        """ 
            getDataFrame3
            Returns a single dataframe containing all of the data needed
            for the third visualization - the area chart.
        """
        #TODO
        return None

