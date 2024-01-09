import arcpy, os

# Input feature class or layer
input_fc = os.path.join(r"C:\Stuff\DR-AKSHAY\NEW\LAMS\Toolbox\DATA\LAMS_map_print.gdb" ,"Hoshiarpur_wgs84")

# Attribute field name and its value to query
attribute_field = "Site"
attribute_value = "Hoshiarpur"

# Create a SQL expression to query features
sql_expression = "{} = '{}'".format(arcpy.AddFieldDelimiters(input_fc, attribute_field), attribute_value)

# Use a search cursor to query features matching the attribute value
cursor = arcpy.da.SearchCursor(input_fc, ["SHAPE@"], where_clause=sql_expression)

# Initialize variables for extents
x_min = y_min = float('inf')  # Initialize to positive infinity
x_max = y_max = float('-inf')  # Initialize to negative infinity

# Loop through the queried features
for row in cursor:
    geom = row[0]  # Geometry of the feature
    feature_extent = geom.extent  # Extent of the individual feature

    # Update the combined extent
    x_min = min(x_min, feature_extent.XMin)
    y_min = min(y_min, feature_extent.YMin)
    x_max = max(x_max, feature_extent.XMax)
    y_max = max(y_max, feature_extent.YMax)

# Release cursor
del cursor

# Print or use the combined extent
if x_min != float('inf') and y_min != float('inf') and x_max != float('-inf') and y_max != float('-inf'):
    combined_extent = arcpy.Extent(x_min, y_min, x_max, y_max)
    print("Combined Extent:", combined_extent.XMin, combined_extent.YMin, combined_extent.XMax, combined_extent.YMax)
else:
    print("No features found matching the attribute value.")