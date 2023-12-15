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


def txt2csv(path_in, path_out):
    """
    Convert a text file to a CSV file.

    This function checks if the input text file exists, and if so, converts it to a DataFrame
    and then saves it as a CSV file. If the CSV file already exists, it does nothing.

    Args:
        path_in (str): Path to the input text file.
        path_out (str): Path where the output CSV file will be saved.

    Returns:
        pd.DataFrame or None: The converted DataFrame if the file is converted, None otherwise.
    """
    # Check for presence of 'ratings_ba_clean.csv'
    if not os.path.isfile(path_in):
        # Convert .txt to csv
        df = text_to_df(path_in)
        # Convert .txt to csv
        df.to_csv(path_out)
        return df
    else:
        print('.csv already present')
        return None


def csv2cache(df, path_in, cache_path):
    """
    Cache a DataFrame to a pickle file.

    If the pickle file does not exist at the specified path, this function caches the provided DataFrame.
    If the DataFrame is None, it loads it from a CSV file at the given path.

    Args:
        df (pd.DataFrame): The DataFrame to be cached.
        path_in (str): Path to the CSV file, used if df is None.
        cache_path (str): Path where the pickle file will be saved.
    """
    # Check for presence of 'ratings_ba.pkl' (BeerAdvocate)
    if not os.path.isfile(cache_path):
        if df == None:
            # Load the newly created .csv file
            df = pd.read_csv(path_in)

        # Cache the data
        pickle.dump(df, open(cache_path, 'wb'))
    else:
        print('.pkl already present')


FOLDER_RB = './data/RateBeer/'
# Check for presence of 'ratings_rb.pkl' (RateBeer)
if not os.path.isfile('ratings_rb.pkl'):

    # Load the newly created .csv file
    ratings_rb_csv = pd.read_csv('./data/RateBeer/' + 'ratings_rb_clean.csv')

    # Cache the data
    pickle.dump(ratings_rb_csv, open('ratings_rb.pkl', 'wb'))
else:
    print('file already loaded and cached')


def text_to_df(file_path):
    """
    Convert a .txt file to a DataFrame.

    Reads a text file, where each line represents a key-value pair separated by a colon,
    and converts it into a DataFrame. Each block separated by an empty line represents a record.

    Args:
        file_path (str): The path to the .txt file.

    Returns:
        pd.DataFrame: The resulting DataFrame.
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


def data_pre_processing(data_to_merge1, data_to_merge2):
    """
    Merge two DataFrames and preprocess date-related information.

    This function merges two DataFrames on the 'user_id' column, and processes the 'date' and 'joined' columns
    to extract meaningful date-related information such as month, year, and a combined year-month period.

    Args:
        data_to_merge1 (pd.DataFrame): The first DataFrame to merge, typically containing user data.
        data_to_merge2 (pd.DataFrame): The second DataFrame to merge, typically containing ratings data.

    Returns:
        pd.DataFrame: The merged and preprocessed DataFrame.
    """

    user_ratings = data_to_merge1.merge(data_to_merge2, how='right', on='user_id')
    user_ratings['date'] = pd.to_datetime(user_ratings['date'], unit='s')

    user_ratings['joined'] = pd.to_datetime(user_ratings['joined'], unit='s')

    # Create columns 'month', 'year' & 'year_month' on 'user_ratings' dataframe
    user_ratings['month'] = user_ratings['date'].dt.month
    user_ratings['year'] = user_ratings['date'].dt.year

    user_ratings['year_month'] = user_ratings['date'].dt.to_period('M')
    return user_ratings


def extract_country(location):
    """
    Extract the country name from a location string.

    This function splits a location string by a comma and returns the first part, assuming the format
    'Country, OtherInfo'. If there's no comma, it returns the original location string.

    Args:
        location (str): The location string to be processed.

    Returns:
        str: The extracted country name or the original location string if no comma is present.
    """
    if ',' in location:
        # If there is a comma in the location, split the string and take the first part
        return location.split(',')[0].strip()
    else:
        # If there is no comma, return the original location
        return location.strip()


def get_coordinates(country):
    """
    Get geographical coordinates for a given country.

    This function uses the Nominatim geocoder to find the latitude and longitude of a given country.
    In case of failure (e.g., timeout or no result), it returns None for both coordinates.

    Args:
        country (str): The name of the country for which to find coordinates.

    Returns:
        tuple: A tuple containing the latitude and longitude of the country, or (None, None) if not found.
    """
    # Initialize a geolocator using Nominatim with a specific user_agent
    geolocator = Nominatim(user_agent="geoapiExercices")
    try:
        # obtain the location (latitude and longitude) for the given country
        location = geolocator.geocode(country, language='en', timeout=1)
        return (location.latitude, location.longitude)
    except:
        return (None, None)


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
    """
    Convert a country name to its ISO 3166-1 alpha-3 code.

    This function first checks if the country name is in a predefined manual mapping. If not found,
    it then attempts to find the country's ISO 3166-1 alpha-3 code using the pycountry library.

    Args:
        country_name (str): The name of the country.

    Returns:
        str or None: The ISO 3166-1 alpha-3 code of the country if found, None otherwise.
    """
    # Check if the country is in the manual mapping
    if country_name in manual_mapping:
        return manual_mapping[country_name]

    # Try to get the code using pycountry
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except AttributeError:
        return None  # Handle cases where the country name is not found


def plot_map_ratings(user_ratings):
    """
    Create an interactive map showing the distribution of user ratings by country.

    This function counts the number of ratings for each country, calculates the proportion of these
    ratings relative to the total, and plots this data on a world map using Folium. Each country is
    represented by a circle marker, whose size and popup info indicate the count and proportion of ratings.

    Args:
        user_ratings (pd.DataFrame): DataFrame containing user ratings with a 'country' column.

    Returns:
        folium.Map: An interactive map visualizing the ratings distribution.
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
    # display(country_counts)
    # Initialize a Folium map with an initial center at latitude 0 and longitude 0
    m = folium.Map(location=[0, 0], zoom_start=1)

    # Iterate over each row in the country_counts dataFrame
    for _, row in country_counts.iterrows():
        # Check if coordinates for the country are available
        if row['coord'][0] is not None:
            # Add a Circle marker to the map for each country
            folium.Circle(
                location=row['coord'],
                radius=row['count'],
                color='crimson',
                fill=True,
                fill_color='crimson',
                popup='{}: {} %, {} ratings'.format(row['country'], row['proportion'], row['count'])
            ).add_to(m)

    return m


def plot_STL(ratings_per_month, type):
    """
    Plot the Seasonal-Trend decomposition using LOESS (STL) of a time series.

    This function decomposes a time series into three components: trend, seasonality, and residuals,
    and plots these components. It's useful for analyzing and visualizing time series data.

    Args:
        ratings_per_month (pd.Series): Time series data of ratings per month.
        type (str): Color type for the plot.

    """
    # Apply Seasonal-Trend decomposition using LOESS (STL)
    stl = STL(ratings_per_month, seasonal=13, period=12)
    result = stl.fit()  # fit the model

    # Extract components from the decomposition
    trend = result.trend
    seasonal = result.seasonal
    residual = result.resid

    # Create 4 subplot figure
    plt.figure(figsize=(10, 6))

    # Subplot 1: Trend
    plt.subplot(411)
    plt.plot(trend, label='Trend', color=type)
    plt.legend(loc='best')
    plt.grid()

    # Subplot 2: Seasonality
    plt.subplot(412)
    plt.plot(seasonal, label='Seasonality', color=type)
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
    Compute the proportion of monthly ratings for a specific subset of beers.

    This function calculates the proportion of ratings for a subset of beers compared to all beers
    within a given date range, on a monthly basis. It's useful for understanding the popularity of a beer subset over time.

    Args:
        df (pd.DataFrame): The complete DataFrame containing all beer ratings.
        beer_subset (pd.DataFrame): The subset of beers for which to calculate the proportions.
        date_start (int): The starting year for the analysis.
        date_end (int): The ending year for the analysis.

    Returns:
        pd.Series: A series containing the proportion of ratings per month for the beer subset.
    """

    # filter the dataframe information from date_start to date_end
    # for all the beers
    all_beers = df[
        (df['year'] >= date_start) &
        (df['year'] <= date_end)
        ]

    # for the beer subset
    beer_subset = beer_subset[
        (beer_subset['year'] >= date_start) &
        (beer_subset['year'] <= date_end)
        ]

    # Define the number of ratings per month for all beers around the world
    all_beer_ratings = all_beers.groupby('year_month')["rating"].count()

    # Number of ratings per month
    beer_subset_nbr_ratings_per_month = beer_subset.groupby('year_month')["rating"].count()

    # Proportion of number of ratings per month
    beer_subset_prop_nbr_ratings = beer_subset_nbr_ratings_per_month / all_beer_ratings

    return beer_subset_prop_nbr_ratings


def feature_standardized(feature, df, beer_subset, date_start, date_end):
    """
    Compute the standardized value of a specified feature for a beer subset.

    This function calculates the mean and standard deviation of a given feature (e.g., rating, aroma, palate)
    for a subset of beers and returns the standardized (z-score) feature values per month.

    Args:
        feature (str): The feature to standardize (e.g., 'rating').
        df (pd.DataFrame): The complete DataFrame containing all beer data.
        beer_subset (pd.DataFrame): The subset of beers for the analysis.
        date_start (int): The starting year for the analysis.
        date_end (int): The ending year for the analysis.

    Returns:
        pd.Series: A series containing the standardized feature values per month for the beer subset.
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

    # Compute mean and variance of feature for the beer style, in the defined period
    mean_feature = beer_subset[feature].mean()
    std_feature = beer_subset[feature].std()

    # Mean feature value per month
    beer_subset_feature_per_month = beer_subset.groupby('year_month')[feature].mean()

    # z-score of the feature per month
    beer_subset_z_score = (beer_subset_feature_per_month - mean_feature) / std_feature

    return beer_subset_z_score


def plot_seasonal_trends(beer_feature, title, ylabel, color, month_increment=3):
    """
    Plot seasonal trends for a specific feature of a beer subset.

    This function visualizes the seasonal trends of a specified feature (e.g., ratings) for a beer subset.
    It plots the feature values per month and applies seasonal-trend decomposition using LOESS (STL)
    to further analyze the trends.

    Args:
        beer_feature (pd.Series): The feature values per month to plot.
        title (str): The title of the plot.
        ylabel (str): The label for the y-axis.
        color (str): The color of the plot lines.
        month_increment (int): The interval of months to display on the x-axis.

    """

    plt.figure(figsize=(14, 4))
    x = beer_feature.index.astype(str)
    plt.plot(x, beer_feature.values, marker='o', color=color)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.title(title)

    # We show only labels by intervals of 3 months, to have a clearer visualisation
    plt.xticks(rotation=90, fontsize=9)
    tick_positions = range(0, len(x), month_increment)
    plt.xticks(tick_positions, [x[i] for i in tick_positions], rotation=45)

    plt.grid()
    plt.show()

    # Convert the index to timestamp. A new variable is created to avoid changing the original dataframe
    beer_feature_STL = beer_feature.copy()
    beer_feature_STL.index = beer_feature_STL.index.to_timestamp()

    # Plot seasonal trends
    plot_STL(beer_feature_STL, color)
