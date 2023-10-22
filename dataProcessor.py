import json
import pandas as pd

def read_json_file(file_path):

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")
    
def avgAgeCountry(filePath, age_transform=None):
    data = read_json_file(filePath)
    df = pd.DataFrame(data)

    if age_transform is not None:
        df['age'] = df['age'].apply(age_transform)

    try:
        avg_age = df.groupby('country')['age'].mean().to_dict()
        return avg_age
    except KeyError:
        return {}

def calculateTotalAge(filePath, country):
    data = read_json_file(filePath)
    
    if not data:
        return 0 

    df = pd.DataFrame(data)
    total_age = df.loc[df['country'] == country, 'age'].sum()
    return total_age

def countUsersByCountry(filePath):
    data = read_json_file(filePath)
    
    if not data:
        return {}  

    df = pd.DataFrame(data)
    user_counts = df['country'].value_counts().to_dict()
    return user_counts

def yearsToMonths(age):
    return age * 12

