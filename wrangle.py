import env as e
import pandas as pd
import numpy as np
import os
# import splitting functions
from sklearn.model_selection import train_test_split

def wrangle_zillow():
    #url and sql pull
    url = e.get_db_url('zillow')
    df = pd.read_sql("""
select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
from propertylandusetype
	join properties_2017
		using (propertylandusetypeid)
WHERE propertylandusedesc = ("Single Family Residential")
""",url)

    #dropping nulls
    df = df.dropna()
    
    #changing value types
    df.yearbuilt = df.yearbuilt.astype(int)
    df.bedroomcnt = df.bedroomcnt.astype(int)
    df.fips = df.fips.astype(int)
    df.taxvaluedollarcnt = df.taxvaluedollarcnt.astype(int) 
    df.calculatedfinishedsquarefeet = df.calculatedfinishedsquarefeet.astype(int)
    
    return df

def splitting_data(df, col):
    '''
    Splitting data function takes in two arguments, one dataframe and the column you want to stratify on. After receiving these two arguments, the first split occurs and splits the data 60/40 for the train portion of the returns. A second split is performed on the remaining 40% of the data at a 50/50 ratio to make sure the validate and test returns are equal size. Random state of 24 because Kobe. Returns all 3 data sets.
    '''
    #first split
    train, validate_test = train_test_split(df,
                     train_size=0.6,
                     random_state=24,
                     stratify=df[col]
                    )
    #second split
    validate, test = train_test_split(validate_test,
                                     train_size=0.5,
                                      random_state=24,
                                      stratify=validate_test[col]
                                     )
    return train, validate, test