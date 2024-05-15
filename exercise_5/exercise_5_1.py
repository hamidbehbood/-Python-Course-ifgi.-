from qgis.PyQt.QtWidgets import QInputDialog, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject, QgsGeometry, QgsFeatureRequest

# Accessing the "Muenster_City_Districts" layer
dlayer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
slayer = QgsProject.instance().mapLayersByName("Schools")[0]

# Getting features of "Muenster_City_Districts" layer
features = dlayer.getFeatures()

# Initialize an empty list to store district names
districts_names = []

# Iterate over features to extract district names
for feature in features:
    # Assuming the district name is stored in an attribute named "Name"
    district_name = feature['Name']
    districts_names.append(district_name)

# Sort the district names alphabetically
districts_names.sort()

# Get parent window
parent = iface.mainWindow()

# Show the input dialog to select a district
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District:",  districts_names)

# Check if the user clicked OK and the selected district is valid
if bOk and sDistrict:
    # Select features in the 'dlayer' (Muenster_City_Districts layer) based on the provided district name
    selection = dlayer.selectByExpression(" \"name\" = '{}' ".format(sDistrict), QgsVectorLayer.SetSelection)

    # Zoom to the selected features on the map canvas
    mc.zoomToSelected()

    # Initialize an empty string to store school names
    school_names = ""
    
    # Get the first selected feature from the 'dlayer' (Muenster_City_Districts layer)
    selected = dlayer.selectedFeatures()[0]

    # Get the geometry (polygon) of the selected feature, which represents the selected district
    selection_area = selected.geometry()

    # Iterate over features in the 'slayer' (presumably the "Schools" layer)
    for school_feature in slayer.getFeatures():
        # Get the geometry (point) of the current school feature
        school_geometry = school_feature.geometry()
    
        # Check if the geometry of the current school feature is within the geometry of the selected district
        if school_geometry.within(selection_area):
            
            #  Calculate distances to the district centroid
            centroid_selected_district = selection_area.centroid()
            distances = round(centroid_selected_district.distance(QgsGeometry.fromPointXY(school_geometry.asPoint())) / 1000, 2)
            # Concatenate the name and type of the current school feature,distance to the center and add double line breaks
            school_names += school_feature['NAME'] + ", " + school_feature['SchoolType'] + "\n " +" distantce from the center: " +str(distances) +"km"+"\n\n   "
            
          
            

# Call the function
            # Show a message box with the school names
    QMessageBox.information(parent, "Schools in " + sDistrict, school_names)
elif not bOk:
    # Show a warning message if the user cancels the process
    QMessageBox.warning(parent, "Schools", "User cancelled")
