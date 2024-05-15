from qgis.PyQt.QtWidgets import QInputDialog, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject, QgsGeometry, QgsFeatureRequest ,QgsCoordinateTransform,QgsCoordinateReferenceSystem ,QgsPointXY
# Import re for using spilt method for breaking a string into two parts
import re

# opening QInput window for user to write the Input 
parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")

# spliting the input into  two different string
latitude_longitude_List = re.split(',', sCoords)

# change the string into floats
latitude_longitude_List[0]=float(latitude_longitude_List[0])
latitude_longitude_List[1]=float(latitude_longitude_List[1])

# Assign the two CRS that we want to use in this part 
crsTO = QgsCoordinateReferenceSystem("EPSG:25832")
crsFrom = QgsCoordinateReferenceSystem("EPSG:4326")

# Using Transform method to change the points coordinates based on desired CRS 
transformation = QgsCoordinateTransform(crsFrom, crsTO, QgsProject.instance())
pointFrom =  QgsPointXY(latitude_longitude_List[1], latitude_longitude_List[0])
pointTo = transformation.transform(pointFrom)
point_geom = QgsGeometry.fromPointXY(pointTo)



# Create a map canvas object
mc = iface.mapCanvas()

# Get Muenster_City_Districts layer in the TOC
layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# puting the Features of  Muenster_City_Districts in a variable
Features=layer.getFeatures()
# Flag for the next chapter to show if the coordinates is in the city or not 
Notfound=1
# a loop for analysis of going throug every disstrict polygon to see if point is part of that or not
for feature in Features:
        if (feature.geometry().contains(point_geom)==True):
            QMessageBox.information(parent, "Result", "The coordinates are within a Münster city district.")
            print("The coordinates are within a Münster city district.")
            Notfound=0
            break
# a statment that pops up when The coordinates are not within a Münster city district.             
if (Notfound==1):
         QMessageBox.information(parent, "Result", "The coordinates are not within a Münster city district.")
         print("The coordinates are not within a Münster city district.")