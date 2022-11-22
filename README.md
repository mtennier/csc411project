# csc411project

# information
Visualizations for 411 project, written in Python.

# county voter data comes from:
https://www.elections.ny.gov/EnrollmentCounty.html
(Feb 2021 data)

# grad rate data comes from:
https://data.nysed.gov/downloads.php
(Grad Rate Database)

# fips numbers are needed for the first visualization, the file we used can be found here:
https://data.ny.gov/w/juva-r6g2/caer-yrtv?cur=FHSIbLUwMDP&from=VgnqclHtMDJ


# INSTALLATION

# install pip
https://packaging.python.org/en/latest/tutorials/installing-packages/
(follow the commands given under the "Ensure you can run pip from the command line")

# you also need anaconda:
https://docs.anaconda.com/anaconda/install/windows/
(install for macos and linux on the side - you also need anaconda for the csc421 a4 assignment)

# finally you need to install plotly - run this command on the command line
pip install plotly==5.11.0

# to run (ofc in the directory with all the code):
py CityvsRural.py

# to "fake" only showing one county's data:
 1 - click on the county - the counties I have selected are "St.Lawrence" and "Suffolk" however if you want to
 do a different one I can either change it for you or you can replace the county name in the equals
 2 - uncomment either line 31 or line 35 depending on which county you clicked
 3 - rerun the code

# to "fake" clicking on a point
1 - click on one of the points on the graph - right now it is set up for the point labelled "Academy School"
however if you want to do a different one or I included some comments on how to edit it in the code
2 - uncomment line 23
3 - rerun the code

# more of these can be added if you would like it to show a different idea, just let me know or you can also
# try editing the statements based on the code comments. I can also record these parts.

# Also full screen before recording anything - thing get really compressed if you dont.