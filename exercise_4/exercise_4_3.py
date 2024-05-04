# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
import os

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS/QGIS", True)

#Finding the shape files in the directory and put them in list with thier path 
Munster_Shape_File=[]
Munster_Shape_File_dir=[]
Munster_Shape_File_Name=[]
Munster_dir=[]
Munster_dir = r"/Users/hamidrezabehbood/Downloads/Muenster"
Munster_files = os.listdir(Munster_dir)

for Item in range(len(Munster_files)):
    if(Munster_files[Item].endswith(".shp")==True):
        Munster_Shape_File.append(Munster_files[Item])
        Munster_Shape_File_dir.append(Munster_dir+"/"+Munster_files[Item])
        Shape_File_Temp=''
        for chr in Munster_files[Item]:
          if chr == '.':
            break
          else: 
           Shape_File_Temp+=chr
        Munster_Shape_File_Name.append(Shape_File_Temp)
       
for Item in range(len(Munster_Shape_File)):  
    print(Munster_Shape_File[Item])
    print(Munster_Shape_File_dir[Item])
    print(Munster_Shape_File_Name[Item])



 
   
 # Path to data and QGIS-project



layer_path = r"/Users/hamidrezabehbood/Downloads/Muenster/Schools.shp"
project_path = r"/Users/hamidrezabehbood/Downloads/"  # for QGIS version 3+

# Create layer
layer = QgsVectorLayer(layer_path, "WKA eingeladen", "ogr")

# Check if layer is valid
if not layer.isValid():
    print("Error loading the layer!")
else:
    # Create QGIS instance and "open" the project
    project = QgsProject.instance()
    project.read(project_path)

    # Add layer to project
    project.addMapLayer(layer)

    # Save project
    project.write()

    print("Layer added to project\nProject saved successfully!")
