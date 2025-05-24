"""
Program: Commodity Data Visualization
Author: Charvi Poshala
File Name: commodityDataVisualization_charvi_07.py
Description: This script processes a CSV file containing product price information. It cleans and organizes the data, then filters 
             and visualizes the price trends for a specified product in a chosen city. The plot includes formatted axes for better
             readability and insights.

Revisions:  
    00: Load and clean the CSV data for analysis
    01: Structure the data to include product names, dates, farm prices, and city prices
    02: Filter and sort the data for a specific product and city
    03: Identify the number of distinct products and count their occurrences
    04: Extract the lowest price for a product (e.g., Oranges) in a city (e.g., Chicago)
    05: Compare the lowest city price to the farm price for the same product
    06: Calculate the average price of a product (e.g., Peaches) in a particular city (e.g., Atlanta)
    07: Compute the duration of availability for each product based on the date range
"""

import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Revision 00: Load and clean the CSV data
def read_and_clean_data(file_path):
    cleaned_data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read header row
        for row in reader:
            # Revision 01: Clean and structure data
            product_name = row[0]
            date_parsed = datetime.strptime(row[1], "%m/%d/%Y")  # Convert date string to datetime object
            farm_price = float(row[2].strip('$'))  # Convert farm price to float
            city_prices = [float(price.strip('$')) for price in row[3:]]  # Convert city prices to float
            cleaned_data.append((product_name, date_parsed, farm_price, *city_prices))
    return cleaned_data, headers

# Revision 02: Filter and sort data for specific product and city
def filter_data(data, product_name, city_index):
    filtered = [
        (entry[1], entry[city_index + 3])  # Extract date and city price
        for entry in data if entry[0].lower() == product_name.lower()  # Match product name (case-insensitive)
    ]
    return sorted(filtered, key=lambda x: x[0])  # Sort by date

# Revision 04: Plot price trends
def plot_data(filtered_data, product_name, city_name):
    dates, prices = zip(*filtered_data)  # Separate dates and prices
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, marker='o', label=f'{product_name} in {city_name}')
    plt.title(f'Price Trend for {product_name} in {city_name}')
    plt.xlabel('Date')
    plt.ylabel('Price (in $)')
    plt.grid(visible=True)
    plt.legend()

    # Format y-axis to display prices with a dollar sign
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:.2f}'))

    # Format x-axis ticks
    if len(dates) > 10:
        plt.xticks(dates[::len(dates) // 10], rotation=45)  # Show a subset of dates
    else:
        plt.xticks(rotation=45)  # Rotate all dates if fewer ticks

    plt.tight_layout()
    plt.show()

# Main Code
file_path = '/Users/charviposhala/Downloads/produce_csv.csv'  # Path to the CSV file

# Revision 00: Clean the data
cleaned_data, headers = read_and_clean_data(file_path)

# Debugging: Display headers for verification
print(f"Headers: {headers}")

# Define the product and city for analysis
product_name = "Oranges"
city_name = "Chicago"

# Revision 02: Get the column index for the selected city
city_index = headers.index(city_name) - 3  # Adjust for header offset
print(f"City Column Index: {city_index}")

# Revision 02: Filter data for the product and city
filtered_data = filter_data(cleaned_data, product_name, city_index)

# Revision 04: Visualize the filtered price trends
plot_data(filtered_data, product_name, city_name)
