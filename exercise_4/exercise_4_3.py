# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
import os

# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS/QGIS", True)

# Finding the shape files in the directory and put them in list with thier path 

# Initialize the variable that we need 
# The list to store only the shape files of directory 
Shape_File=[]
# The list to store directory of only the shape files in Shape_file list.
Shape_File_dir=[]
# The list to store only the name of the Shape_file list without the shffix .shp
Shape_File_Name=[]
# The main directory that we want to look into and serach for the shape files 
Munster_dir = r"/Users/hamidrezabehbood/Downloads/Muenster"
# Storing all the above directory files into a list
All_Directory_Files = os.listdir(Munster_dir)

#A foor loop to store the .shp files,  Names,Directory path and Name without suffix into three different list that we Initialized above.
for Item in range(len(All_Directory_Files)):
  # Finding every .shp files base on the suffix 
    if(All_Directory_Files[Item].endswith(".shp")==True):
      # Add the file names with the suffux into a list
        Shape_File.append(All_Directory_Files[Item])
        # Making the directoy path to the files and saving them into a spreate list with the same indxing as the files names 
        Shape_File_dir.append(Munster_dir+"/"+All_Directory_Files[Item])
        # Making a list of files name without suffix into a list 
        # The method works with the . as the braking point and save the files name as it reach the .
        Shape_File_Temp=''
        for chr in All_Directory_Files[Item]:
          if chr == '.':
            break
          else: 
           Shape_File_Temp+=chr
        # Adding the name to a list by append method
        Shape_File_Name.append(Shape_File_Temp)


# A test that shows the result        
#for Item in range(len(Shape_File)):  
   # print(Shape_File[Item])
   #print(Shape_File_dir[Item])
   # print(Shape_File_Name[Item])





 # Path to data and QGIS-project
project_path = r"/Users/hamidrezabehbood/Downloads/Munster_Data.qgz"  # for QGIS version 3+
# A loop that make raw string add add the layers by their own names. 
Number_of_loops= 0
for layers in range(len(Shape_File_dir)):
  # Building an empty raw strring  
  layer_path = r"z" 
  # Replacing the empty raw string with the real directory
  layer_path =layer_path.replace( 'z', Shape_File_dir[layers]) 
  # Using the files names as the layers names 
  layers_name =Shape_File_Name[layers]
  # Create layer
  layer = QgsVectorLayer(layer_path, layers_name, "ogr")
  # Check if layer is valid
  if not layer.isValid():
    print("Error loading the layer!")
  else:
    Number_of_loops+=1
    # Create QGIS instance and "open" the project
    project = QgsProject.instance()
    project.read(project_path)
    # Add layer to project
    project.addMapLayer(layer)
    project.write()
    print(f"{ 'Layer ' + str(Number_of_loops)+ ' added to project' }")
  
print("Layers added to project\nProject saved successfully!")
