import geopandas as gpd
import numpy as np
import json
import pandas as pd
import os

folder_path = 'geojson'  # Replace with the path to your folder containing GeoJSON files

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Exclude 'info1123.geojson' from the list
files = [file for file in files if file.endswith('.geojson') and file != 'info1123.geojson']

# Filter only GeoJSON files
species = [file.split('.')[0] for file in files if file.endswith('.geojson')]

print(species)

# Load GeoJSON file
file_path = 'geojson/Sorbusaucuparia1123.geojson'
gdf = gpd.read_file(file_path)
# Exclude 'geometry' column
columns_to_process = [col for col in gdf.columns if col != 'geometry']
gdf = gdf[columns_to_process]
#gdf = pd.DataFrame(columns=gdf_t.columns[:-1])  # Exclude the last column 'geometry'
print(gdf)
gdf.to_csv('test.csv')

# Function to calculate mean for a matrix
def calculate_mean(matrix):
    try:
        numeric_matrix = np.array(json.loads(matrix))
        return np.mean(numeric_matrix)
    except:
        print(f"Error decoding JSON:")
        return np.nan  # or handle the error in another way

mean_df = pd.DataFrame()

for specie in species:
    # Load GeoJSON file
    file_path = f'geojson/{specie}.geojson'
    gdf = gpd.read_file(file_path)
    # Exclude 'geometry' column
    columns_to_process = [col for col in gdf.columns if col != 'geometry']
    gdf = gdf[columns_to_process]

    mean_rows = []
    # Iterate through features and calculate mean
    for index, row in gdf.iterrows():
        row_values = {}
        for column in gdf.columns:
            matrices = row[column]
            #print(matrices)
            #band_number = int(column.split('_')[-1]) if '_' in column else 1  # Extract band number from column name
            #for matrix_index, matrix in enumerate(matrices):
            mean_value = calculate_mean(matrices)
            row_values[column] = mean_value
            print(f"Location {index + 1} , Band {column}: Mean = {mean_value}")

        # Append the row to the list
        mean_rows.append(row_values)
    # Create the DataFrame from the list of rows
    mean_df_iter = pd.DataFrame(mean_rows)
    mean_df_iter['tag']= specie
    mean_df = pd.concat([mean_df,mean_df_iter])

mean_df.to_csv('test_tag.csv')