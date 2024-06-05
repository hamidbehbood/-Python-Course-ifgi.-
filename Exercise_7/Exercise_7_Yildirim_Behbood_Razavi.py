from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import time
import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing, QgsProject, QgsVectorLayer, QgsCoordinateTransform, QgsPointXY, 
    QgsRectangle, QgsProcessingParameterFileDestination, QgsFeatureSink, 
    QgsCoordinateReferenceSystem, QgsProcessingException, QgsFeatureRequest, 
    QgsProcessingAlgorithm, QgsProcessingParameterString, 
    QgsProcessingParameterEnum, QgsProcessingParameterFeatureSource, 
    QgsProcessingParameterFeatureSink
)
from qgis import processing
from qgis.utils import iface

class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    """
    Algorithm to generate a PDF profile for a specific city district.
    """
    
    DISTRICT_NAME = 'DISTRICT_NAME'
    POINT_INPUT = 'POINT_INPUT'
    PDF_OUTPUT = 'PDF_OUTPUT'
    
    def create_pdf(self, output_path, attribute_dict, picture_path, line_height=20):
        """
        Generates a PDF with district information.
        :param output_path: Path to save the PDF
        :param attribute_dict: Dictionary containing district attributes
        :param picture_path: Path to the district map image
        :param line_height: Distance between lines of text
        """
        pdf_canvas = canvas.Canvas(output_path, pagesize=letter)
        
        # Set title font and write title
        pdf_canvas.setFont("Times-Roman", 22)
        pdf_canvas.drawString(150, 760, f"Information for the district '{attribute_dict['district_name']}'")
        
        # Set content font
        pdf_canvas.setFont("Times-Roman", 16)
        
        # Write general information about the district
        self._write_district_info(pdf_canvas, 100, 735, attribute_dict, line_height)
        
        # Draw image of the district map if picture_path is provided
        if picture_path:
            pdf_canvas.drawString(100, 600, "Map of selected district:")
            pdf_canvas.drawImage(picture_path, 100, 270, width=400, height=300)
        
        # Save the PDF document
        pdf_canvas.save()

    def _write_district_info(self, pdf_canvas, x, y, attribute_dict, line_height):
        """
        Writes the district information on the PDF canvas.
        :param pdf_canvas: The canvas to write on
        :param x: The x coordinate to start writing
        :param y: The y coordinate to start writing
        :param attribute_dict: Dictionary containing district attributes
        :param line_height: Distance between lines of text
        """
        # Write parent district
        pdf_canvas.drawString(x, y, f"The parent district is: {attribute_dict['parent']}.")
        y -= line_height
        # Write area
        pdf_canvas.drawString(x, y, f"The district has an area of {attribute_dict['area']} m^2.")
        y -= line_height
        # Write house number count
        pdf_canvas.drawString(x, y, f"The district has {attribute_dict['house_number_count']} house numbers.")
        y -= line_height
        # Write parcels count
        pdf_canvas.drawString(x, y, f"The district contains {attribute_dict['parcels_count']} parcels.")
        y -= line_height
        
        # Write counted property (Pools or Schools)
        if attribute_dict['counted_property'] != "None":
            pdf_canvas.drawString(x, y, f"The counted property is '{attribute_dict['counted_property']}'. There are {attribute_dict['pool_or_school_count']} objects of this property.")
        else:
            pdf_canvas.drawString(x, y, "Please select pools or schools as point input.")

    def capture_district_image(self, selected_district):
        """
        Captures an image of the district's map.
        :param selected_district: The selected district feature
        :return: Path to the saved image
        """
        districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        district_geometry = selected_district.geometry()
        
        # Set up coordinate reference system transformations
        crs_layer = districts_layer.crs()
        crs_target = QgsCoordinateReferenceSystem(3857)
        transformation = QgsCoordinateTransform(crs_layer, crs_target, QgsProject.instance())
        
        # Get the bounding box of the district
        bbox = district_geometry.boundingBox()
        point_lb = transformation.transform(QgsPointXY(bbox.xMinimum(), bbox.yMinimum()))
        point_rt = transformation.transform(QgsPointXY(bbox.xMaximum(), bbox.yMaximum()))
        
        # Create transformed bounding box and set map extent
        transformed_bbox = QgsRectangle(point_lb, point_rt)
        iface.mapCanvas().setExtent(transformed_bbox)
        iface.mapCanvas().refresh()
        
        # Wait for the map to render
        time.sleep(5)
        
        # Save the map as an image
        image_path = os.path.join(QgsProject.instance().homePath(), "map.png")
        iface.mapCanvas().saveAsImage(image_path)
        
        return image_path
    
    def tr(self, string):
        """
        Translates a string.
        :param string: The string to translate
        :return: Translated string
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateCityDistrictProfile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'create_city_district_profile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localized.
        """
        return self.tr('Layer Tools')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localized.
        The group ID should be unique within each provider. Group ID should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'layer_tools'

    def shortHelpString(self):
        """
        Returns a localized short helper string for the algorithm. This string
        should provide a basic description of what the algorithm does and the
        parameters and outputs associated with it.
        """
        return self.tr("This processing script creates a PDF profile for a specific city district.")
    
    def get_alphabetical_district_list(self):
        """
        Returns a list of district names in alphabetical order.
        :return: List of district names
        """
        districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        
        # Set up request to order district names alphabetically
        request = QgsFeatureRequest()
        order_by_clause = QgsFeatureRequest.OrderByClause("Name", ascending=True)
        order_by = QgsFeatureRequest.OrderBy([order_by_clause])
        request.setOrderBy(order_by)

        # Extract district names into a list
        district_names = [feature['NAME'] for feature in districts_layer.getFeatures(request)]
        return district_names
    
    def initAlgorithm(self, config=None):
        """
        Defines inputs and output of the algorithm.
        """
        district_names = self.get_alphabetical_district_list()
        
        # Add district name parameter
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DISTRICT_NAME,
                self.tr('District Name'),
                district_names
            )
        )
        
        # Add point input parameter (pools or schools)
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POINT_INPUT,
                self.tr('Input point layer. Select Pools or Schools'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        # Add PDF output parameter
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.PDF_OUTPUT,
                self.tr('PDF Output'),
                fileFilter='PDF files (*.pdf)'
            )
        )
    
    def count_features_within_district(self, layer_name, district_geometry):
        """
        Counts the number of features within the given district.
        :param layer_name: Name of the layer to count features from
        :param district_geometry: Geometry of the district
        :return: Number of features within the district
        """
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        layer.removeSelection()
        
        # Select features within the district geometry
        for feature in layer.getFeatures():
            if feature.geometry().within(district_geometry):
                layer.selectByIds([feature.id()], QgsVectorLayer.AddToSelection)
                
        return layer.selectedFeatureCount() if layer.selectedFeatureCount() > 0 else 0

    def processAlgorithm(self, parameters, context, feedback):
        """
        Main algorithm processing.
        """
        district_names = self.get_alphabetical_district_list()
        districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        
        # Get the selected district name
        district_name_index = self.parameterAsInt(parameters, 'DISTRICT_NAME', context)
        district_name = district_names[district_name_index]
        
        # Select the district by name
        districts_layer.selectByExpression(f"\"Name\" = '{district_name}'", districts_layer.SetSelection)
        selected_district = districts_layer.selectedFeatures()[0]
        parent_district = selected_district["P_District"]
        district_geometry = selected_district.geometry()
        district_area = district_geometry.area()
        
        # Count house numbers in the district
        house_number_count = self.count_features_within_district('House_Numbers', district_geometry)
        
        # Count parcels in the district
        parcels_layer = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0]
        parcels_layer.removeSelection()
        parcels_layer.selectByExpression(f"\"Name\" = '{district_name}'", parcels_layer.SetSelection)
        parcels_count = parcels_layer.selectedFeatureCount()
        
        # Determine the type of point input (Pools or Schools) and count features
        point_input_layer_path = self.parameterAsCompatibleSourceLayerPath(parameters, 'POINT_INPUT', context, compatibleFormats=['shp'])
        if point_input_layer_path.endswith("public_swimming_pools.shp"):
            counted_property = "Pools"
            property_count = self.count_features_within_district('public_swimming_pools', district_geometry)
        elif point_input_layer_path.endswith("Schools.shp"):
            counted_property = "Schools"
            property_count = self.count_features_within_district('Schools', district_geometry)
        else:
            counted_property = "None"
            property_count = 0
            
        # Get the output path for the PDF
        pdf_output_path = self.parameterAsFileOutput(parameters, 'PDF_OUTPUT', context)
        
        # Collect district information into a dictionary
        district_info = {
            'district_name': district_name,
            'parent': parent_district,
            'area': district_area,
            'house_number_count': house_number_count,
            'parcels_count': parcels_count,
            'counted_property': counted_property,
            'pool_or_school_count': property_count
        }
        
        # Capture the district image
        district_image_path = self.capture_district_image(selected_district)
        
        # Create the PDF
        self.create_pdf(pdf_output_path, district_info, district_image_path)
        
        # Return results for debugging
        return {
            'PDF_OUTPUT': pdf_output_path,
            'Point': point_input_layer_path,
            'district_name': district_name,
            'parent': parent_district,
            'area': district_area,
            'house_number_count': house_number_count,
            'parcels_count': parcels_count,
            'counted_property': counted_property,
            'pool_or_school_count': property_count
        }
