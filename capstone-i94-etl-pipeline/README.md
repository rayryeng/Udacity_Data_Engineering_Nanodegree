# Udacity Provided Project

For this nanodegree, I decided not to create my own project and went ahead with
completing the project provided by Udacity. For this project, some datasets
were made available and was open-ended. I decided to create an ETL pipeline
as well as designing a data model following the star schema to incorporate
I94 immigration and city demographic data. This data model will ultimately be
used for creating a database that can be used to answer questions that are
related to immigration behaviour.

A template notebook was made available, which I have modified to complete the
ETL pipeline and data model. The data model and database was stored on Amazon
Redshift to allow for fast and multi-threaded queries.

Please note that due to the large size of the data, this workspace is designed
to be run on the Udacity workspace and no attempts should be made to run this
locally on your own computer. You can look at the
`Capstone_Project_Final.ipynb` notebook for more details, including a more
detailed description of each datasets used as well as the completed ETL
pipeline and data quality checks.

## Some Notes

- Because this will ultimately connect with Amazon Redshift, this requires
  AWS credentials. The `dwh.cfg` is for you to fill out with the proper
  information so that the notebook can complete the connection to AWS and
  transfer the dataframes over to Redshift as tables. Have a look at the
  _Moving the data onto Redshift_ section of the notebook for more details. The
  file is intentionally blank on purpose due to its sensitive nature.

- You will require installing the
  [`pandas-redshift`](https://github.com/agawronski/pandas_redshift) helper
  package that allows transferring Pandas dataframes from a notebook onto
  AWS Redshift. It simplifies the ETL process by automatically figuring out
  the right requirements to create staging tables to house the data frame, then
  allow the transfer of data from the staging tables to Redshift. Just in case,
  there is a cell in the notebook at the very beginning that runs a `pip install`
  to load the package for use.

# Description of the data used

## I94 Immigration Data

This data comes from the US National Tourism and Trade Office. A data dictionary
is included in the workspace. There's also a sample file so you can take
look at the data in CSV format before reading it all in. However, the entire
dataset was not needed to be used. Only a subset of the dataset was used in
this project, which was the data during April 2016. Due to the large nature
of the data, this can be accessed on the Udacity workspace where this notebook
was hosted. You can access the immigration data in a folder on the Udacity
workspace with the following path: `../../data/18-83510-I94-Data-2016/`.
There's a file for each month of the year. The file name that I used was
`i94_apr16_sub.sas7bdat`. Each file has a three-letter abbreviation for the
month name. So a full file path for June would look like this:
`../../data/18-83510-I94-Data-2016/i94_jun16_sub.sas7bdat`.

Note: these files are large, so if you decide to read the data in one go, it
will take roughly 15-20 minutes on the Udacity workspace to load the dataframe
in.

Below is what it would look like to import this file into pandas.

```python
fname = '../../data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat'
df = pd.read_sas(fname, 'sas7bdat', encoding="ISO-8859-1")
```

## U.S. City Demographic Data

This data comes from OpenSoft. contains various information about the
demographics of all US cities and census-designated places with a population
greater or equal to 65,000. This comes from the 2015 American Community Survey
from the US Census Bureau's 2015 American Community Survey.

# Instructions

All you have to do is run the notebook from start to finish. Make sure that you
fill out the `dwh.cfg` file with the proper AWS credentials and bucket locations
so that the notebook can run successfully.

## Note on the data

I've included all of the other data that was provided by Udacity for the project
that I didn't end of using, which includes airport codes and temperature data.
If you decide not to use the data I've used for the project and modify it
for your own use, please go right ahead.
