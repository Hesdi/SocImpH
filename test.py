import pandas as pd
#Fair Market Value
HIGHEST_FMV = {"Szerdahelyi utca.":'381.25%'}
LOWEST_FMV = { "Reguly Antal utca." :"46.02%"}
currstreet = "Baross"
def get_street_price_change(file_path, street_name):
    # Read the CSV file
    try:
        data = pd.read_csv(file_path)
    # Filter data for 2015 and 2022
        data_2015 = data[data['record_year'] == 2015]
        data_2022 = data[data['record_year'] == 2022]

        # Filter data for streets that contain the partial street name
        data_2015 = data_2015[data_2015['street'].str.contains(street_name, case=False, na=False)]
        data_2022 = data_2022[data_2022['street'].str.contains(street_name, case=False, na=False)]


        # Check if data is available for both years
        if not data_2015.empty and not data_2022.empty:
            avg_price_2015 = data_2015['all_avg_price_per_nm'].iloc[0]
            avg_price_2022 = data_2022['all_avg_price_per_nm'].iloc[0]

            # Calculate the percentage change
            percentage_change = ((avg_price_2022 - avg_price_2015) / avg_price_2015) * 100
            
            return percentage_change.round(2)
        else:
            return None

    except FileNotFoundError:
        return None

# Example usage of the function
file_path = 'residential_property_prices.csv'

# print(get_street_price_change(file_path, currstreet))


#Creating job opportunities
census_data = pd.read_csv("census_data.csv")
def calculate_unemployment_education_percentages_district(data, street_input, district):
    """
    Function to calculate the percentages of unemployed individuals among primary, secondary, and higher educated people for a given street name and type in a specific district. The function also expands common street type abbreviations.

    :param data: Pandas DataFrame containing the census data.
    :param street_input: The full name of the street (including type) to perform the analysis for.
    :param district: The district number to filter the data.
    :return: A dictionary with percentages of different education levels being unemployed for the specified street in the specified district.
    """
    # Dictionary to map abbreviations to full street types
    street_type_mapping = {
        "u.": "utca",
        "tér": "tér",
        "krt": "körút"
    }

    # Splitting the street name and type
    split_input = street_input.split(" ")
    street_name = " ".join(split_input[:-1])
    street_type_abbreviation = split_input[-1]

    # Expanding the street type abbreviation
    street_type = street_type_mapping.get(street_type_abbreviation, street_type_abbreviation)

    # Filter data for the specific street and type in the specified district
    filtered_data = data[(data['street'] == street_name) & (data['street_type'] == street_type) & (data['district'] == district)]

    # If no data found for the specific street, return a message
    if filtered_data.empty:
        return f"No data found for {street_input} in district {district}."

    # Extracting data from the filtered DataFrame
    row = filtered_data.iloc[0]
    total_primary_edu = row['primary_education']
    total_secondary_edu = row['secondary_education']
    total_higher_edu = row['higher_education']
    unemployed_total = row['unemployed']

    # Calculating percentages
    percentage_primary_edu_unemployed = (unemployed_total / total_primary_edu) * 100 if total_primary_edu > 0 else 0
    percentage_secondary_edu_unemployed = (unemployed_total / total_secondary_edu) * 100 if total_secondary_edu > 0 else 0
    percentage_higher_edu_unemployed = (unemployed_total / total_higher_edu) * 100 if total_higher_edu > 0 else 0

    return {
        "Percentage of Unemployed Primary Educated": percentage_primary_edu_unemployed.round(2),
        "Percentage of Unemployed Secondary Educated": percentage_secondary_edu_unemployed.round(2),
        "Percentage of Unemployed Higher Educated": percentage_higher_edu_unemployed.round(2)
    }

# Calculate the percentages for "Baross u." in district 8
unemployment_education_percentages_baross_u_district_8 = calculate_unemployment_education_percentages_district(census_data, "Baross u.", 8)
# print(unemployment_education_percentages_baross_u_district_8["Percentage of Unemployed Primary Educated"])


# Accessibility
AVG_BICYCLE_USAGE_IN_8_DIS = 1506.56
HIGHEST_USAGE = 6553
bicycles = pd.read_csv('molbubi_district_8_202105_202310.csv')
def average_bicycle_usage(data, street_name):
    """
    Function to calculate the average bicycle usage for a given street.

    :param data: Pandas DataFrame containing the bicycle usage data.
    :param street_name: The name of the street to calculate the average usage for.
    :return: Average bicycle usage for the specified street.
    """
    # Filter data for the specific street
    street_data = data[data['station'].str.contains(street_name, case=False, na=False)]

    # If no data found for the specific street, return a message
    if street_data.empty:
        return f"No data found for {street_name}."

    # Calculating the average usage
    average_usage = street_data.iloc[:, 1:].mean(axis=1).mean()

    return average_usage

# Example usage of the function
average_usage_baross_utca = average_bicycle_usage(bicycles, "Baross utca")
print(average_usage_baross_utca)


# POIS
LATITUDE = 47.431160
LONGITUDE = 19.104240
import geopandas as gpd
import geopy.distance

def find_pois_categories_within_walking_distance(file_path, target_lat, target_lon, walking_time_minutes=15):
    # Load the POIs data from a GeoJSON file
    pois_data = gpd.read_file(file_path)

    # Define walking speed (5 km/h) and calculate max distance in km
    walking_speed_km_h = 5
    max_distance_km = (walking_time_minutes / 60) * walking_speed_km_h

    # Function to calculate distance between two points
    def calculate_distance(lat1, lon1, lat2, lon2):
        return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

    # Extract latitude and longitude from the 'geometry' column
    pois_data['latitude'] = pois_data['geometry'].y
    pois_data['longitude'] = pois_data['geometry'].x

    # Filter POIs within walking distance and extract categories
    pois_within_walking_distance = pois_data[pois_data.apply(
        lambda row: calculate_distance(target_lat, target_lon, row['latitude'], row['longitude']) <= max_distance_km,
        axis=1
    )]

    return pois_within_walking_distance[['amenity_category', 'joint_amenity']]

# Usage
file_path = 'google_pois_2021.geojson'  # Replace with your file path
target_latitude = 47.431160
target_longitude = 19.104240
categories = find_pois_categories_within_walking_distance(file_path, target_latitude, target_longitude)
print(categories)




