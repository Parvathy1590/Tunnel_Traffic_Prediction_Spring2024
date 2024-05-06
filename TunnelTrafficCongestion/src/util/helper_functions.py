import pandas as pd
import requests as requests
from geopy.geocoders import Nominatim
def read_data(filePath):
    #Using speed data
    #Speed data is in muliple sheets.
    excel_file = pd.ExcelFile(filePath)
    sheets_dict = pd.read_excel(excel_file, sheet_name=None)

    # Merge using concat, all DataFrames in the dictionary into one
    trafficflow_data = pd.concat(sheets_dict.values(), ignore_index=True)
    return trafficflow_data

#1) Convert date columns to datetime format 2) Handle missing values(drop columns with a number of missing values) 3) Handle categorical variables and convert them to numerical( check if needed )
def preprocess(df):
    df['Dato'] = pd.to_datetime(df['Dato']).copy()

    df['Fra'] = pd.to_datetime(df['Fra'], utc=True)
    df['Til'] = pd.to_datetime(df['Til'], utc=True)
    df['Gjennomsnittshastighet'] = pd.to_numeric(df['Gjennomsnittshastighet'], errors='coerce')
    df['85-fraktil'] = pd.to_numeric(df['85-fraktil'], errors='coerce')
    df['Trafikkmengde'] = pd.to_numeric(df['Trafikkmengde'], errors='coerce')

    df['Trafikkmengde'] = df['Trafikkmengde'].replace("-", 0)
    # After conversion, check for any new missing values in 'Gjennomsnittshastighet'
    new_missing_values = df.isnull().sum()
    # Check data types to confirm conversions
    data_types = df.dtypes
    data_types, new_missing_values
    return df

def save_to_csv(df,filePath):
    df.to_csv(filePath,index=False)
    
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location:
        print(f"Coordinates for {location_name}: Latitude {location.latitude}, Longitude {location.longitude}")
        return location.latitude, location.longitude
    else:
        return None    

def callAPI(tunnelName,date,coordinates):
    #coordinates = get_coordinates(tunnelName,date)
    #print(f"DATE is {date}")
    #if coordinates:
       #print(f"Coordinates for {tunnelName}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
   # else:
       #print(f"Coordinates for {tunnelName} not found.")
    
    url = f'https://aa.usno.navy.mil/api/rstt/oneday?date={date} &coords={coordinates[0]},{coordinates[1]}&dst=true'
    # Make the API call
    response = requests.get(url)
    morning=noon=evening=night= None

    if response.status_code == 200: #If succsesful
        data = response.json()
        
    else:
        print("No data")
       
    
    for event in data['properties']['data']['sundata']:
        if event['phen'] == 'Begin Civil Twilight':
            morning = event['time']
        elif event['phen'] == 'Upper Transit':
            noon = event['time']
        elif event['phen'] == 'Set':
            evening = event['time']
        elif event['phen'] == 'End Civil Twilight':
            night = event['time']

    return morning,night


# Function to determine if it's day or night based on a given time and twilight times
def determine_part_of_day(time_str, morning, night):
    # Convert strings to time objects
    
    time = pd.to_datetime(time_str, format="%H:%M:%S").time()
    print
    morning_time = pd.to_datetime(morning, format="%H:%M").time()
    night_time = pd.to_datetime(night, format="%H:%M").time()
    
    # Determine if the time is within day or night
    if morning_time <= time <= night_time:
        return "Day"
    else:
        return "Night"

# Function to process each row and update "PartOfDay"
def update_part_of_day(row):
    tunnel_name = row["Navn"]
    datetime_str = row["Dato"]
    # Split on space
    parts = datetime_str.split(" ")  # Splits into ['2022-01-04', '00:00:00']

    date_part = parts[0]  # '2022-01-04
    
    # Get twilight times using the simulated API call
    morning, night = callAPI(tunnel_name, date_part)
    
    # Determine if it's day or night based on "Fra tidspunkt"
    return determine_part_of_day(date_part, morning, night)

def write_to_file(filename, modelName, data_dict): 
    # Check if the file exists and remove it if it does

    # Open the file in append mode
    with open(filename, "a") as file:
        # Write tunnel name to the file
        file.write(f"Model Name: {modelName}\n\n")

        # Write key-value pairs from data_dict to the file
        for key, value in data_dict.items():
            file.write(f"{key}: {value}\n")

        # Add a new line after writing all key-value pairs
        file.write("\n")


