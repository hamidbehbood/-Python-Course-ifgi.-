# Using QVariant ensures that data is processed correctly and interpreted correctly by QGIS.
from PyQt5.QtCore import QVariant

from qgis.core import (
    QgsProject, # Represents a QGIS project and is used to add or remove layers from the project.
    QgsVectorLayer, # Represents vector data layers. It is used to create a new layer in memory or load an existing layer.
    QgsFeature, # Represents a single feature in a layer. Geometry and attributes are defined using this class and added to the layer.
    QgsGeometry, # Represents geometric data. Used to create geometry from WKT (Well-Known Text) or other formats.
    QgsField, # Used to add new fields (attributes) to layers. The name, type, and other properties of each field are defined using this class.
    QgsFields,
    QgsWkbTypes,# Represents Well-Known Binary (WKB) geometry types. Used to identify and convert geometry types.
    QgsVectorFileWriter
)

# Creating a layer called temp_standard_land_value_muenster.
layer = QgsVectorLayer("MultiPolygon?crs=epsg:25832", "temp_standard_land_value_muenster", "memory")

# dataProvider is required for operations such as adding, updating or deleting data to the layer.
pr = layer.dataProvider()

# Creating the fields of new layer
fields = [
    QgsField('standard_land_value', QVariant.Double),
    QgsField('type', QVariant.String),
    QgsField('city_district', QVariant.String)
]

# Add fields to layer
pr.addAttributes(fields)

# Apply field updates to the layer and make them visible in the QGIS interface
layer.updateFields()

# Path of csv file
csv_file_path = "C:/Users/LENOVO/Desktop/Master/PythonArcGIS_QGIS/exercises_6/Data for Session 6/standard_land_value_muenster.csv"

# Read the csv file
with open(csv_file_path, 'r') as file:
    lines = file.readlines() # The readlines() method reads all the lines of a file and returns them as a list.

# Create a dictionary to store geometries by name
geometries_by_name = {}

# Add the csv lines to the new layer with for loop
for line in lines[1:]:  # Skip the first line since it is title
    # Remove leading and trailing whitespace characters from the line, 
    # then split the line into a list of substrings using ';' as the delimiter
    data = line.strip().split(';')
    name = data[2]  
    
    # Extract the well-known text (WKT) geometry from geometry
    wkt = data[3]
    # Create a QgsGeometry object from the WKT representation
    geom = QgsGeometry.fromWkt(wkt)
    
    

    # Create a new QgsFeature object to represent a feature (or geometry with attributes) in the layer
    feature = QgsFeature()
    feature.setGeometry(geom)
    feature.setAttributes([float(data[0].replace(',', '.')), name, data[2]])

    pr.addFeature(feature)


# Add the layer to map
QgsProject.instance().addMapLayer(layer)