import warnings
import pandas as pd
from textblob import TextBlob
warnings.filterwarnings('ignore')
import re


def column_work(df):

    num_mon = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    
    columns_to_keep = ['Title', 'Airline', 'Reviews',
        'Type of Traveller', 'Month Flown', 'Route', 'Class', 'Seat Comfort', 
        'Staff Service', 'Food & Beverages', 'Inflight Entertainment',
        'Value For Money', 'Overall Rating', 'Recommended']

    df = df[columns_to_keep]

    df['Year Flown'] = df['Month Flown'].str.split().str[1]
    df['Month Flown'] = df['Month Flown'].str.split().str[0].map(num_mon)

    df.head()

    return df



def blob_function(df):

    # extract the comments and ratings into a list

    ratings = df['Overall Rating'].to_list()
    comments = df['Reviews'].to_list()

    # create a blank list to hold the blob

    polarities = []
    subjectivities = []

    # Analyze the sentiment of each comment

    for comment in comments:
      blob = TextBlob(comment)
      polarity = blob.sentiment.polarity
      subjectivity = blob.sentiment.subjectivity
      polarities.append(polarity)
      subjectivities.append(subjectivity)
    
      print(f"Comment: {comment}")
      print(f"Polarity: {polarity}")
      print(f"Subjectivity: {subjectivity}")
      print()

    # add values to new df columns

    df['Polarity'] = pd.Series(polarities)
    df['Subjectivity'] = pd.Series(subjectivities)

    return df

# split the route column #2
def split_to_via(df):
    # Split the text based on separators (to, via)
    split_values = df['Route'].str.split(r'(?<=\bto\b)|(?<=\bvia\b)', expand=True)
    
    # remove to and via from the split columns
    split_values = split_values.apply(lambda x: x.str.replace(r'\bto\b|\bvia\b', '', regex=True))
    
    # Create new columns and load in the split values
    df['Origin'] = split_values[0].str.strip()
    df['Destination'] = split_values[1].str.strip()
    
    # Check if the 'Via' column exists and handle multiple cities
    if 2 in split_values.columns:
        df['Via'] = split_values[2].str.replace('/', '').str.split().str[0].str.strip()
    else:
        df['Via'] = ''
    
    return df


# begin the one hot encoding #4

def one_hot_e (df):
    # get dummies 
    df = pd.get_dummies(df, columns = ['Class', 'Type of Traveller'])
    return df


def col_work_dos(df):
    #drop some columns
    
    df_renew = df[[ 'Airline', 'Month Flown', 'Year Flown', 'Seat Comfort',
       'Staff Service', 'Food & Beverages', 'Inflight Entertainment',
       'Value For Money', 'Overall Rating', 'Recommended', 
       'Origin', 'Destination', 'Via', 'Comment Polarity',
       'Comment Subjectivity', 'Title Polarity', 'Title Subjectivity',
       'Class_Business Class', 'Class_Economy Class', 'Class_First Class',
       'Class_Premium Economy', 'Type of Traveller_Business',
       'Type of Traveller_Couple Leisure', 'Type of Traveller_Family Leisure',
       'Type of Traveller_Solo Leisure']]
    
    
    # reformat recommended column values
    df_renew ['Recommended'] = df_renew['Recommended'].replace({'no':0, 'yes':1})

    return df_renew

airport_codes = pd.read_csv('Resources/airports_utf.csv')

def lookup_code(airport_string):
    if len(airport_string) == 3 and airport_string.isupper():
        return airport_string
    else: 
        code = airport_codes.loc[airport_codes["City"] == airport_string, "Code"]
        if code.empty:    # because .loc returns series (vs string), can't run "not code" instead run code.empty
            print(f'could not find code for {airport_string}')
            return None
        display(code)
        return code.iloc[0]
        
def lookup_city(airport_string):
    if len(airport_string) == 3 and not airport_string.isupper():
        # city = airport_codes.loc[airport_codes['Code'] == airport_string, 'City']
        return airport_string
    else: 
        city = airport_codes.loc[airport_codes["Code"] == airport_string, "City"]
        if city.empty:  
            print(f'could not find city for {airport_string}')
            return None
        display(city)
        return city.iloc[0]
    
def find_airport_code(origin, airport_codes):
       airports_origins = airport_codes['City'].unique()
       if origin in airports_origins:
           city_rows = airport_codes[airport_codes['City'] == origin]
           if not city_rows.empty:
               return city_rows['Code'].values[0]
       return origin

def find_airport_city(origin, airport_codes):
    airports_origins = airport_codes['Code'].unique()
    if origin in airports_origins:
        city_rows = airport_codes[airport_codes['Code'] == origin]
        if not city_rows.empty:
            return city_rows['True_City'].values[0]
    city_rows = airport_codes[airport_codes['City'] == origin]
    if not city_rows.empty:
        return city_rows['True_City'].values[0]


        # def split_to_via(df, column):
#     # Split the text based on separators (to, via)
#     split_values = df[column].str.split(r'(?<=\bto\b)|(?<=\bvia\b)', expand=True)
    
#     # remove to and via from the split columns
#     split_values = split_values.apply(lambda x: x.str.replace(r'\bto\b|\bvia\b', '', regex=True))
    
#     # Create new columns and load in the split values
#     df['Origin'] = split_values[0].str.strip()
#     df['Destination'] = split_values[1].str.split().str.join(' ').str.strip()
#     df['Via'] = split_values[2].str.split().str.join(' ').str.strip()
    
#     return df

def split_via(row):
    # Define the user-defined separators
    user_seps = r'[/&-and]'
    
    # Use regular expression to split on any user-defined separator
    split_values = re.split(user_seps, row['Via'], maxsplit=1)
        
    # If the split returns more than one value, return the split values
    if len(split_values) > 1:
       return split_values
    # If no separator found, return the original value and None
    else:
        return [row['Via'], None]
    
def split_via_2(row):
    if pd.notnull(row['Via']):  # Check if the value is not None
        via = row['Via'].split(' / ')
        if len(via) > 1:
            row['Via'] = via[0]
            row['Via_2'] = via[1]
        else:
            row['Via_2'] = None
    return row