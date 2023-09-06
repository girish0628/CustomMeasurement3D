# ExportShapefile - Created by Jeff Hanson, HFM
# Purpose:  to export selected featues to a usernamed shapefile as a geoprocessing servie
# Note:  the output directory is PortalShapeFiles on Hertzgis server, a shared folder

import datetime
import arcpy
import os
import json
import sys
import zipfile
arcpy.env.overwriteOutput = True

####################################
# setting variable default values
####################################
arcpy.AddMessage("Default scratch GDB is:")
arcpy.AddMessage(arcpy.env.scratchGDB)
arcpy.AddMessage("*******************************")

# Excel table output folder
exportFolder = arcpy.env.scratchGDB
jobsDir = os.path.dirname(os.path.abspath(exportFolder))
arcpy.AddMessage("Export Folder: " + exportFolder)
arcpy.AddMessage("Jobs Dir: " + jobsDir)

# #############################
# # Getting input parameters
# #############################

# arcpy.AddMessage("Collecting input parameters")

# # Get the passed field polygon graphics and user specified shapefile name
# inFeatset = r"C:\Stuff\DR-AKSHAY\LAMS\LAMS-KMLExporter\Toolbox\MyProject5.gdb\Landparcel_F"
# # inFeatset = arcpy.GetParameter(0)
# if inFeatset == '#' or not inFeatset:
#     sys.exit()

# shpFileName = "ester"
# # shpFileName = arcpy.GetParameterAsText(1)
# outputShapeFile = jobsDir + "\\" + shpFileName + ".shp"
# if not shpFileName:
#     sys.exit()
# arcpy.AddMessage("Output file is " + outputShapeFile)

# #############################
# # start main proccess
# #############################

# try:
#     arcpy.AddMessage("Running shapefile export to create " + outputShapeFile)

#     arcpy.CopyFeatures_management(inFeatset, outputShapeFile)

#     arcpy.AddMessage("Created shapefile: " + outputShapeFile)

#     # put the files that make up the shapefile into a zip file
#     zip = zipfile.ZipFile(jobsDir + "\\" + shpFileName +
#                           ".zip", 'w', zipfile.ZIP_DEFLATED)
#     for file in os.listdir(jobsDir):
#         if file.startswith(shpFileName):
#             if not file.endswith(".zip"):
#                 print(os.path.join(jobsDir, file))
#                 zip.write(os.path.join(jobsDir, file))
#     zip.close()
#     arcpy.AddMessage("Zip file created.")

#     outputFile = jobsDir + "\\" + shpFileName + ".zip"

#     arcpy.AddMessage("Return file is " + outputFile)
#     arcpy.SetParameter(2, outputFile)
# except:
#     arcpy.AddMessage(
#         "Error exporting and downloading shapefile " + outputShapeFile)
#     sys.exit()
req_field = ["business_name", "company_name", "state", "site", "district", "tehshil", "village", "survey_no",
             "parcel_area", "land_type", "acquired_status", "mutation_status", "na_status", "tsr_status"]


def a(path):
    fields = arcpy.ListFields(path)
    for field in fields:
        # print(field.name)
        if field.name not in req_field:
            print(field.name)


kmzFile = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
outputKmzFile = "C:\\Stuff\\DR-AKSHAY\\LAMS\\MyProject6_LAMS\\MyProject6_LAMS\\" + kmzFile + ".kmz"
inFeatset = r"C:\Stuff\DR-AKSHAY\LAMS\LAMS-KMLExporter\Toolbox\MyProject5.gdb\Landparcel_F"
where_clause = "site='{}'".format("ahmedabad airport")
try:
    # Create temporary layer in memory
    temp_lyr = "in_memory/tempOutput"

    # Convert SDE Feature Class to Feature Layer
    arcpy.MakeFeatureLayer_management(
        in_features=inFeatset, out_layer=temp_lyr, where_clause=where_clause)

    arcpy.DeleteField_management(temp_lyr, req_field, "KEEP_FIELDS")

    # fields = arcpy.ListFields(temp_lyr)
    # for field in fields:
    #     # print(field.name)
    #     if field.name not in req_field:
    #         arcpy.DeleteField_management(temp_lyr, field.name)
    #         print(field.name)

    arcpy.LayerToKML_conversion(layer=temp_lyr, out_kmz_file=outputKmzFile)

    arcpy.AddMessage("Export to KML completed successfully.")
    if arcpy.Exists(temp_lyr):
        arcpy.Delete_management(temp_lyr)

    arcpy.AddMessage("Created KMZ export: " + outputKmzFile)

    arcpy.AddMessage("Return file is " + outputKmzFile)
    arcpy.SetParameter(1, outputKmzFile)
except Exception as error:
    print('Caught this error: ' + repr(error))
# except:
#     arcpy.AddMessage(
#         "Error exporting and downloading shapefile " + outputKmzFile)
#     sys.exit()
