# import shutil

# src = 'C:\Stuff\DR-AKSHAY\LAMS\LAMS-MAP-PRINT\output1.pdf'
# dst = 'C:\Stuff\DR-AKSHAY\LAMS\LAMS-MAP-PRINT\output_new.pdf'
# shutil.move(src, dst)


import arcpy
arcpy.env.workspace = r"C:\Users\giris\Documents\ArcGIS\Projects\KML\KML.gdb"

# arcpy.MakeFeatureLayer_management("Hoshiarpur_wgs", "Hoshiarpur_wgs_lyr")
# arcpy.MakeFeatureLayer_management("village_boundary_r_wgs", "village_boundary_r_wgs_lyr")
import arcpy

# Set the workspace where your feature class is located
arcpy.env.workspace = r"C:\path\to\your\geodatabase.gdb"

# Specify the names of the source and destination feature classes
source_feature_class = "village_boundary_r_wgs"
destination_feature_class = "Hoshiarpur_wgs"

# Create an insert cursor for the destination feature class
with arcpy.da.InsertCursor(destination_feature_class, ["SHAPE@"]) as dest_cursor:
    # Create a search cursor for the source feature class
    with arcpy.da.SearchCursor(source_feature_class, ["SHAPE@"]) as source_cursor:
        for source_row in source_cursor:
            # Insert the row into the destination feature class
            dest_cursor.insertRow(source_row)

print("Geometry inserted successfully.")

