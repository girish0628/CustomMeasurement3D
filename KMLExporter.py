# ExportShapefile - Created by GIRISH LGEOM
# Purpose:  to export selected feature to a KMZ as a Geoprocessing Service
# Note:  the output directory is a shared folder

import arcpy
import os
import sys
import zipfile
import datetime
arcpy.env.overwriteOutput = True

####################################
# setting variable default values
####################################
arcpy.AddMessage("Default scratch GDB is:")
arcpy.AddMessage(arcpy.env.scratchGDB)
arcpy.AddMessage("*******************************")

# KMZ File output folder
exportFolder = arcpy.env.scratchGDB
jobsDir = os.path.dirname(os.path.abspath(exportFolder))
arcpy.AddMessage("Export Folder: " + exportFolder)
arcpy.AddMessage("Jobs Dir: " + jobsDir)

#############################
# Getting input parameters
#############################

arcpy.AddMessage("Collecting input parameters")
inSiteName = arcpy.GetParameterAsTexts(0)

inFeatureSet = "SDE Connection Path ?????"
if inFeatureSet == '#' or not inFeatureSet:
    sys.exit()

kmzFile = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# kmzFile = os.path.join(arcpy.env.scratchFolder, "site.kml")
# Site Name
where_clause = "site='{}'".format(inSiteName)


outputKmzFile = jobsDir + "\\" + kmzFile + ".kmz"

arcpy.AddMessage("Output file is " + outputKmzFile)

#############################
# start main proccess
#############################

try:
    arcpy.AddMessage("Running KMZ export to create " + outputKmzFile)

    # Create temporary layer in memory
    temp_lyr = "memory/tempParReg"

    # Convert SDE Feature Class to Feature Layer
    arcpy.MakeFeatureLayer_management(
        in_features=inFeatureSet, out_layer=temp_lyr, where_clause=where_clause)

    # Get input feature class and output KML file names
    # output_kml_file = parameters[1].valueAsText + ".kml"

    # Convert feature class to KML
    # arcpy.LayerToKML_conversion(input_feature_class, output_kml_file)
    arcpy.LayerToKML_conversion(layer=temp_lyr, out_kmz_file=outputKmzFile)

    arcpy.AddMessage("Export to KML completed successfully.")
    if arcpy.Exists(temp_lyr):
        arcpy.Delete_management(temp_lyr)

    arcpy.AddMessage("Created KMZ export: " + outputKmzFile)

    arcpy.AddMessage("Return file is " + outputKmzFile)
    arcpy.SetParameter(1, outputKmzFile)
except:
    arcpy.AddMessage(
        "Error exporting and downloading shapefile " + outputKmzFile)
    sys.exit()
