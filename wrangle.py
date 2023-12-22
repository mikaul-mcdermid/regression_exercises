import env as e
import pandas as pd
import numpy as np
import os
# import splitting functions
from sklearn.model_selection import train_test_split

def get_zillow_data():
    filename = 'zillow.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        url = e.get_db_url('zillow')
        sql_query = ("""
select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
from properties_2017
WHERE propertylandusetypeid = 261
""")
    df = pd.read_sql(sql_query, url)
    df.to_csv(filename)
    return df    

def wrangle_zillow():
    """
    This function acquires and prepares the Zillow dataset for analysis.

    If the 'zillow.csv' file exists, the function reads the data from the CSV file.
    If the file does not exist, it reads the data from the 'zillow' database using SQL queries
    and saves the resulting DataFrame to 'zillow.csv'.

    The function then drops any rows with missing values and performs necessary data type conversions
    on the 'yearbuilt', 'bedroomcnt', 'fips', 'taxvaluedollarcnt', and 'calculatedfinishedsquarefeet' columns.

    Returns:
    - pd.DataFrame: The prepared and cleaned Zillow dataset.

    Example:
    df_zillow = wrangle_zillow()
    """
    # acquire the data
    filename = 'zillow.csv'
    if os.path.exists(filename):
        print('this file exists, reading from csv')
        #read from csv
        df = pd.read_csv(filename, index_col=0)
    else:
        print('this file doesnt exist, reading from sql and saving to csv')
        #read from sql
        url = env.get_db_url('zillow')
        df = pd.read_sql('''select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
        from propertylandusetype
        join properties_2017
            using (propertylandusetypeid)
        WHERE propertylandusedesc = ("Single Family Residential");''', url)
        #save to csv
        df.to_csv(filename)

    df = df.dropna()

    df.yearbuilt = df.yearbuilt.astype(int)
    df.bedroomcnt = df.bedroomcnt.astype(int)
    df.fips = df.fips.astype(int)
    df.taxvaluedollarcnt = df.taxvaluedollarcnt.astype(int)
    df.calculatedfinishedsquarefeet = df.calculatedfinishedsquarefeet.astype(int)

    return df

def prep_zillow(df):
    df = df.rename(columns={'bedroomcnt':'bedrooms',
                       'bathroomcnt':'bathrooms',
                       'calculatedfinishedsquarefeet':'area',
                       'taxvaluedollarcnt':'salesamount',
                       'fips':'county'})
    df.county = df.county.map({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    return df

def splitting_data(df):
    '''
    Prepare the Telco dataset by cleaning and transforming the data.

    Parameters:
    - df (DataFrame): The input DataFrame containing Telco data.

    Returns:
    - DataFrame: The cleaned and transformed Telco DataFrame.

    Steps:
    1. Drop unnecessary columns: 'payment_type_id', 'internet_service_type_id', 'contract_type_id'.
    2. Replace any empty spaces in 'total_charges' with '0.0'.
    
    Example:
        telco_data = pd.read_csv('telco.csv')
        cleaned_telco = prep_telco(telco_data)
    '''

    #first split
    train, validate_test = train_test_split(df,
                     train_size=0.6,
                     random_state=24,
                    )
    
    #second split
    validate, test = train_test_split(validate_test,
                                     train_size=0.5,
                                      random_state=24,
                                     )
    return train, validate, test

def X_y_split(df, target):
    train, val, test = split_data(df)
    X_train = train.drop(columns=target)
    y_train = train[target]
    X_val = val.drop(columns=target)
    y_val = val[target]
    X_test = test.drop(columns=target)
    y_test = test[target]
    print(f'X_train --> {X_train.shape}')
    print(f'X_val --> {X_val.shape}')
    print(f'X_test --> {X_test.shape}')
    
    return X_train, y_train, X_val, y_val, X_test, y_test

def visualize(df):
    """
    Creates visualizations for our dataframe to visualize relationships between categorical and continuous variables.
    Excludes categorical columns for plotting.
    """
    # Identify continuous columns
    continuous_cols = [col for col in df.columns if df[col].dtype != 'category' and col != 'county']

    for col in continuous_cols:
        # Example function call to plot categorical and continuous variables (replace with your plot function)
        # Assuming you have a function plot_categorical_and_continuous_vars that accepts two columns for plotting
        # Replace `plot_categorical_and_continuous_vars` with your actual plotting function
        plot_categorical_and_continuous_vars(df, df['county'], df[col])


# def wrangle_zillow():
#     #dropping nulls
#     df = df.dropna()
    
#     #changing value types
#     df.yearbuilt = df.yearbuilt.astype(int)
#     df.bedroomcnt = df.bedroomcnt.astype(int)
#     df.fips = df.fips.astype(int)
#     df.taxvaluedollarcnt = df.taxvaluedollarcnt.astype(int) 
#     df.calculatedfinishedsquarefeet = df.calculatedfinishedsquarefeet.astype(int)
    
#     #changing column names
#     df = df.rename(columns={'bedroomcnt':'bedrooms',
#                        'bathroomcnt':'bathrooms',
#                        'calculatedfinishedsquarefeet':'area',
#                        'taxvaluedollarcnt':'salesamount',
#                        'fips':'county'})
    
#     #changing the county to an actual area 
#     df.county = df.county.map({6037:'LA', 6059:'Orange', 6111:'Ventura'})
#     return df

# def splitting_data(df, col):
#     '''
#     Splitting data function takes in two arguments, one dataframe and the column you want to stratify on. After receiving these two arguments, the first split occurs and splits the data 60/40 for the train portion of the returns. A second split is performed on the remaining 40% of the data at a 50/50 ratio to make sure the validate and test returns are equal size. Random state of 24 because Kobe. Returns all 3 data sets.
#     '''
#     #first split
#     train, validate_test = train_test_split(df,
#                      train_size=0.6,
#                      random_state=24,
#                      stratify=df[col]
#                     )
#     #second split
#     validate, test = train_test_split(validate_test,
#                                      train_size=0.5,
#                                       random_state=24,
#                                       stratify=validate_test[col]
#                                      )
#     return train, validate, test


# def wrangle_exams():
#     '''
#     read csv from url into df, clean df, and return the prepared df
#     '''
#     # Read csv file into pandas DataFrame.
#     file = "https://gist.githubusercontent.com/ryanorsinger/\
# 14c8f919920e111f53c6d2c3a3af7e70/raw/07f6e8004fa171638d6d599cfbf0513f6f60b9e8/student_grades.csv"
#     df = pd.read_csv(file)
#     #replace blank space with null value
#     df.exam3 = df.exam3.replace(' ', np.nan)
#     #drop all nulls
#     df = df.dropna()
#     #change datatype to exam1 and exam3 to integers
#     df.exam1 = df.exam1.astype(int)
#     df.exam3 = df.exam3.astype(int)
#     return df


# def regression_split(df):
#     '''
#     Splitting data function takes in two arguments, one dataframe and the column you want to stratify on. After receiving these two arguments, the first split occurs and splits the data 60/40 for the train portion of the returns. A second split is performed on the remaining 40% of the data at a 50/50 ratio to make sure the validate and test returns are equal size. Random state of 24 because Kobe. Returns all 3 data sets.
#     '''
#     #first split
#     train, validate_test = train_test_split(df,
#                      train_size=0.6,
#                      random_state=24,
#                     )
#     #second split
#     validate, test = train_test_split(validate_test,
#                                      train_size=0.5,
#                                       random_state=24,
#                                      )
#     return train, validate, test