# splitting to/from/via

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