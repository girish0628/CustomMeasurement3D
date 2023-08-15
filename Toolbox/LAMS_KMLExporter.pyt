# -*- coding: utf-8 -*-

import os
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "KML-Exporter"
        self.alias = "KMLExporter"

        # List of tool classes associated with this toolbox
        self.tools = [KMLExporter]


class KMLExporter(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export to KML"
        self.description = "Exports an SDE feature class to KML format."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # params = arcpy.Parameter(
        #     displayName="Input Feature Class",
        #     name="input_feature_class",
        #     datatype="DEFeatureClass",
        #     parameterType="Required",
        #     direction="Input")

        In_SiteName = arcpy.Parameter(
            displayName="Site Name",
            name="input_site_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # Out_KML = arcpy.Parameter(
        #     displayName="Output KML FIle",
        #     name="input_kml",
        #     datatype="GPKMLLayer",
        #     parameterType="Required",
        #     direction="Output")
        return [In_SiteName]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """Execute the tool"""
        try:
            kmlFile = os.path.join(arcpy.env.scratchFolder, "site.kml")
            # Site Name
            where_clause = "site='{}'".format(parameters[0].valueAsText)

            # SDE Connection file
            SDE_FC = r"C:\Stuff\DR-AKSHAY\LAMS\LAMS-KMLExporter\Toolbox\MyProject5.gdb\Landparcel_F"

            # Create temporary layer in memory
            temp_lyr = "memory/tempParReg"

            # Convert SDE Feature Class to Feature Layer
            arcpy.MakeFeatureLayer_management(
                in_features=SDE_FC, out_layer=temp_lyr, where_clause=where_clause)

            # Get input feature class and output KML file names
            # output_kml_file = parameters[1].valueAsText + ".kml"

            # Convert feature class to KML
            # arcpy.LayerToKML_conversion(input_feature_class, output_kml_file)
            arcpy.LayerToKML_conversion(
                layer=temp_lyr, out_kmz_file=kmlFile)

            arcpy.AddMessage("Export to KML completed successfully.")
        except Exception as e:
            arcpy.AddError(str(e))

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
