import warnings
import pandas as pd
from textblob import TextBlob
warnings.filterwarnings('ignore')

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


def column_work(df):
    
    #create new db with only the needed columns
    
    df_new = df[['Title', 'Airline', 'Reviews',
       'Type of Traveller', 'Month Flown', 'Route', 'Class', 'Seat Comfort',
       'Staff Service', 'Food & Beverages', 'Inflight Entertainment',
       'Value For Money', 'Overall Rating', 'Recommended']]
    
    #split the month flown column into two and make the month into a number
        # first map the month names to their numbers

    num_mon = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

    df_new['Year Flown'] = df_new['Month Flown'].str.split().str[1]
    df_new['Month Flown'] = df_new['Month Flown'].str.split().str[0].map(num_mon)

    df_new.head()

    return df_new


def split_to_via(df, column):
    # Split the text based on separators (to, via)
    split_values = df[column].str.split(r'(?<=\bto\b)|(?<=\bvia\b)', expand=True)
    
    # remove to and via from the split columns
    split_values = split_values.apply(lambda x: x.str.replace(r'\bto\b|\bvia\b', '', regex=True))
    
    # Create new columns and load in the split values
    df['Origin'] = split_values[0].str.strip()
    df['Destination'] = split_values[1].str.split().str.join(' ').str.strip()
    df['Via'] = split_values[2].str.split().str.join(' ').str.strip()
    
    return df

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
    
