# Accesing the "Schools" layer
layer = QgsProject.instance().mapLayersByName("Schools")[0]

# Path to the *.csv file
# Please adapt the path according to your computer
csv_file_path = r'C:\Users\LENOVO\Desktop\Master\PythonArcGIS_QGIS\exercises_4\SchoolReport.csv'

# Open the csv file in write mode
with open(csv_file_path, 'w') as csv_file:
    # Write header line
    csv_file.write("Name;X;Y\n")
    
    # Getting features of "Schools" layer
    features = layer.getFeatures()
    
    # Loop through the features, perform geometry computation and write to the csv file
    for f in features:
        # Get the geometry of the current feature
        geom = f.geometry()

        # Get the value of the 'NAME' attribute of the current feature
        name = f.attribute('NAME')

        # Get the X coordinate of the geometry's center point
        x = geom.asPoint().x()

        # Get the Y coordinate of the geometry's center point
        y = geom.asPoint().y()
        
        # Write to csv file
        csv_file.write(f"{name};{x};{y}\n")
