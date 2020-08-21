"""Functions to read and format Texas COVID-19 data provided by the 
Texas Department of State Health Services.

Data available online at: 
https://dshs.texas.gov/coronavirus/additionaldata.aspx"""
import numpy as np
import pandas as pd
import datetime

def _tx_county_names():
    return pd.read_csv("data/texas_county_names.csv", header=None)[0].tolist()
    
def read(fi, county_names=_tx_county_names()):
    df = pd.read_excel(
        fi, 
        skiprows=[0],
        header=None)

    # remove rows that contain NaN's:
    if "Notes" in df.iloc[:, 0].tolist():
        df = df.iloc[:, 1:]
    df = df.dropna(axis=0)
        
    # the first dataframe row contains the information we want to
    # eventually become the column headers. First the information
    # needs to be massaged:
    old_cols = df.iloc[0,1:]
    new_cols = []
    for col in old_cols:
        if type(col) == datetime.datetime:
            x = col.strftime("%Y-%m-%d")
        elif "Tests Through" in col:
            x = col.split("Through")[-1]
            x = x.replace("*", "")
            x = x.lstrip(" ") #remove leading whitespace
            x = "%s 2020" %x
            x = datetime.datetime.strptime(x, "%B %d %Y")
        else:
            x = col.split("\n")[-1]
            x = x.split(" ")[-1]
            x = x.replace("*", "")

            # try various ways to get date object:
            if "2020" in x:
                x = datetime.datetime.strptime(x, "%m/%d/%Y")
                x = x.strftime("%Y-%m-%d")
            else:
                x = "2020-%s" %x 
        
        # keep new column header:
        new_cols.append(x)
        
    # set dataframe columns to the massaged headers:
    new_cols = ["county"] + new_cols
    df.columns = new_cols

    # ignore old first row:
    df = df.iloc[1:, :]

    # process index:
    df.loc[:, "county"] = df.county.apply(lambda x: x.lower().capitalize())
    df = df.set_index("county")

    # only keep rows that are Texas counties:
    df = df.loc[county_names, :].copy()
    
    # remove random strings:
    df = df.replace("--", np.nan)
    df = df.replace("-", np.nan)

    # return dataframe:
    return df



