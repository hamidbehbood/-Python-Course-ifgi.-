import processing
import geopandas as gpd
from qgis.core import QgsProject

# Accessing the loaded layers
schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]
district_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# Define a temporary file path for the output
temp_output = '/vsimem/output.shp'

# Processing and storing the output in a temporary file
processing.run("qgis:countpointsinpolygon", 
    {'POLYGONS': district_layer, 
    'POINTS': schools_layer, 
    'FIELD': 'NUMPOINTS', 
    'OUTPUT': temp_output})

# Convert the result layer to a GeoDataFrame
result_gdf = gpd.read_file(temp_output)

# Get the unique values in the P_District column and remove numeric prefix
districts = result_gdf['P_District'].unique()
districts = [district.split(' ', 1)[1] for district in districts]

# Calculate the total NUMPOINTS for each district
district_counts = {}
for district in districts:
    total_points = result_gdf[result_gdf['P_District'].str.contains(district)]['NUMPOINTS'].sum()
    district_counts[district] = total_points

# Print the results in the desired format
for district, count in district_counts.items():
    print(f"{district}: {count}")

