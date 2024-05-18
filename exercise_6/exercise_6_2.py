from qgis.core import QgsProject, QgsField, QgsFeature, QgsVectorLayer, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils, QgsVectorLayerUtils
from PyQt5.QtCore import QVariant

# Load the layer
pools_layer = QgsProject.instance().mapLayersByName('public_swimming_pools')[0]
pools_layer.startEditing()
# Step 1: Update 'Type' column
for feature in pools_layer.getFeatures():
    if (feature['Type'] == 'H'):
        feature.setAttribute(feature.fieldNameIndex('Type'), 'Hallenbad')
    elif (feature['Type'] == 'F'):
        feature.setAttribute(feature.fieldNameIndex('Type'), 'Freibad')
    pools_layer.updateFeature(feature)
# Step 2: Add a new 'district' column
pools_layer.dataProvider().addAttributes([QgsField("district", QVariant.String, len=50)])
# Prepare to find which district each pool is in
district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

# Step 3: Identify district for each pool and update the 'district' column
for pool in pools_layer.getFeatures():
    # Create a point geometry from the pool feature
    point = pool.geometry()
    for district in district_layer.getFeatures():
        if district.geometry().contains(point):
            pool['district'] = district['Name']
            pools_layer.updateFeature(pool)
            break  # Stop the loop once the district is found
# save the changes 
pools_layer.commitChanges()