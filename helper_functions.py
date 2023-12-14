import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
import os
from geopy.geocoders import Nominatim
import folium
import pycountry

def text_to_df (file_path):
    """
    Convert .txt files to dataframes,
    which will then be converted to csv afterwards
    """
    # List to keep dictionaries for each beer
    beers_dic = []

    # A temporary dictionary to store data for each beer
    current_beer = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split the line using the first colon found
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                # Add/update the key in the current beer dictionary
                current_beer[key] = value
           # If you encounter an empty line, it signifies the end of a beer record
            if line.strip() == '':
                beers_dic.append(current_beer)
                current_beer = {}

   # Make sure to add the last beer if the file doesn't end with an empty line
    if current_beer:
        beers_dic.append(current_beer)

 # Create a DataFrame from the list of beer dictionaries
    return pd.DataFrame(beers_dic)

def extract_country(location):
    if ',' in location:
        # If there is a comma in the location, split the string and take the first part
        return location.split(',')[0].strip()
    else:
        # If there is no comma, return the original location
        return location.strip()
        
def get_coordinates(country):
    # Initialize a geolocator using Nominatim with a specific user_agent
    geolocator = Nominatim(user_agent="geoapiExercices")
    try:
        # obtain the location (latitude and longitude) for the given country
        location = geolocator.geocode(country, language='en')
        return (location.latitude,location.longitude)
    except:
        return (None,None)

manual_mapping = {
    'England': 'GBR',
    'Russia': 'RUS',
    'Scotland': 'GBR',
    'Northern Ireland': 'GBR',
    'Taiwan': 'TWN',
    'Czech Republic': 'CZE',
    'Venezuela': 'VEN',
    'Turkey': 'TUR',
    'Aotearoa': 'NZL',
    'Svalbard and Jan Mayen Islands': 'SJM',
    'Bolivia': 'BOL',
    'Wales': 'GBR',
    'Vietnam': 'VNM',
    'Heard and McDonald Islands': 'HMD',
    'Fiji Islands': 'FJI',
    'Slovak Republic': 'SVK',
    'Macedonia': 'MKD',
    'Tanzania': 'TZA',
    'Moldova': 'MDA',
    'South Georgia and South Sandwich Islands': 'SGS',
    'Palestine': 'PSE',
    'Malvinas': 'FLK',
    'Sint Maarten': 'SXM',
}

# Function to convert country name to ISO3166-1-Alpha-3 code
def get_alpha3_code(country_name):
    # Check if the country is in the manual mapping
    if country_name in manual_mapping:
        return manual_mapping[country_name]

    # Try to get the code using pycountry
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except AttributeError:
        return None  # Handle cases where the country name is not found

def plot_map_ratings (user_ratings):
    """
    Create maps using geopy
    """
    # Count the number of ratings for each country
    country_counts = user_ratings['country'].value_counts().reset_index()
    # Rename columns
    country_counts.columns = ['country', 'count']
    # Add a new column proportion
    country_counts['proportion'] = round(100 * country_counts['count'] / country_counts['count'].sum(), 2)
    # Add a new column proportion
    country_counts['coord'] = country_counts['country'].apply(get_coordinates)
    country_counts.country = country_counts.country.apply(get_alpha3_code)
    #display(country_counts)
    # Initialize a Folium map with an initial center at latitude 0 and longitude 0
    m = folium.Map(location=[0,0],zoom_start=1)

    # Iterate over each row in the country_counts dataFrame
    for _, row in country_counts.iterrows():
        # Check if coordinates for the country are available
        if row['coord'][0] is not None:
            # Add a Circle marker to the map for each country
            folium.Circle(
                location = row['coord'],
                radius = row['count'],
                color = 'crimson',
                fill = True,
                fill_color= 'crimson',
                popup='{}: {} %, {} ratings'.format(row['country'], row['proportion'], row['count'])
            ).add_to(m)

    return m

def plot_STL(ratings_per_month, type):
    """
    Plot the general trends, the seasonal trends, and the noise
    """
    # Apply Seasonal-Trend decomposition using LOESS (STL)
    stl = STL(ratings_per_month, seasonal=13, period=12)
    result = stl.fit() # fit the model

    # Extract components from the decomposition
    trend = result.trend
    seasonal = result.seasonal
    residual = result.resid

    # Create 4 subplot figure
    plt.figure(figsize=(10, 6))

    # Subplot 1: Trend
    plt.subplot(411)
    plt.plot(trend, label='Trend', color = type)
    plt.legend(loc='best')
    plt.grid()

    # Subplot 2: Seasonality
    plt.subplot(412)
    plt.plot(seasonal,label='Seasonality', color = type)
    plt.legend(loc='best')
    plt.grid()

      # Subplot 3: Residuals
    plt.subplot(413, sharey=plt.gca())
    plt.plot(residual, label='Residuals', color=type)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.grid()

    # Subplot 4: Placeholder for potential additional plots
    plt.subplot(414)
    plt.axis('off')

def proportion_nbr_ratings(df, beer_subset, date_start, date_end):
    """
    Compute the proportion of number of ratings for a beer subset

    Given a subset of beers, a start date and end date, returns the proportion of number of ratings per month
    (i.e. number of ratings of the beer subset normalized according to the number of ratings for all beers)
    of the subset in the given period.
    
    df: global dataframe, considering all the beers
    beer_subset: subset of beers (generally a subset of df)
    date_start: first date to consider
    date_end: last date to consider
    """
    
    # filter the dataframe information from date_start to date_end
    #for all the beers
    all_beers = df[
        (df['year'] >= date_start) &
        (df['year'] <= date_end)
    ]
    
    #for the beer subset
    beer_subset = beer_subset[
        (beer_subset['year'] >= date_start) &
        (beer_subset['year'] <= date_end)
    ]

    #Define the number of ratings per month for all beers around the world
    all_beer_ratings = all_beers.groupby('year_month')["rating"].count() 
    
    #Number of ratings per month
    beer_subset_nbr_ratings_per_month = beer_subset.groupby('year_month')["rating"].count()

    #Proportion of number of ratings per month
    beer_subset_prop_nbr_ratings = beer_subset_nbr_ratings_per_month / all_beer_ratings
    
    return beer_subset_prop_nbr_ratings

def feature_standardized(feature, df, beer_subset, date_start, date_end):
    """
    Compute the standardized feature (e.g. standardized rating, aroma, palate...) for a beer subset

    Given a subset of beers, a start date and end date, returns the standardized feature mean(rate, aroma, palate...) per month
    (i.e. z-scores), of the subset in the given period.
    """
    
    # filter the dataframe information from date_start to date_end
    all_beers = df[
        (df['year'] >= date_start) &
        (df['year'] <= date_end)
    ]
    
    beer_subset = beer_subset[
        (beer_subset['year'] >= date_start) &
        (beer_subset['year'] <= date_end)
    ]
    
    #Compute mean and variance of feature for the beer style, in the defined period
    mean_feature = beer_subset[feature].mean()
    std_feature = beer_subset[feature].std()

    #Mean feature value per month
    beer_subset_feature_per_month = beer_subset.groupby('year_month')[feature].mean()

    #z-score of the feature per month
    beer_subset_z_score = (beer_subset_feature_per_month - mean_feature) / std_feature
    
    return beer_subset_z_score

def plot_seasonal_trends(beer_feature, title, ylabel, color, month_increment=3):
    """
    Plot the seasonal trends, given roportion of ratings per month, or ratings per month...

    Given a pandas Series showing the feature of a beer subset per month (e.g. rates per month)
    returns plots showing the seasonal trend for this particular feature
    
    beer_feature: pandas Series with per month values
    title: title of the plot
    ylabel: label of the y axis, depending on the chosen feature (e.g. rate, or proportion of number of ratings)
    color: plot color
    month_increment: intervals of month to display. this only affects the labels, not the computation.
    """
    
    plt.figure(figsize = (14,4))
    x = beer_feature.index.astype(str)
    plt.plot(x, beer_feature.values, marker = 'o', color = color)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.title(title)

    #We show only labels by intervals of 3 months, to have a clearer visualisation 
    plt.xticks(rotation = 90, fontsize = 9)
    tick_positions = range(0, len(x), month_increment)
    plt.xticks(tick_positions, [x[i] for i in tick_positions], rotation=45)
    
    plt.grid()
    plt.show()

    #Convert the index to timestamp. A new variable is created to avoid changing the original dataframe
    beer_feature_STL = beer_feature.copy()
    beer_feature_STL.index = beer_feature_STL.index.to_timestamp()

    #Plot seasonal trends
    plot_STL(beer_feature_STL, color)