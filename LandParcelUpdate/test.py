# # import arcpy


# # def read_standalone_table(table_path, field_names, where_clause):
# #     # Create a list to store the data
# #     data = []

# #     # Use a try-except block to handle any potential errors
# #     try:
# #         # Open a search cursor to read the data from the standalone table
# #         with arcpy.da.SearchCursor(table_path, field_names, where_clause) as cursor:
# #             for row in cursor:
# #                 # Process each row and store the data
# #                 data.append(row)

# #     except arcpy.ExecuteError as e:
# #         print("Error occurred: ", e)
# #         return None

# #     return data


# # if __name__ == "__main__":
# #     # Example usage:
# #     arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb"
# #     table_path = "state"  # Change to the name of your standalone table
# #     # Replace with the field names you want to read
# #     field_names = ["state_name"]
# #     where_clause = "id=1"

# #     # Call the function to read data from the standalone table
# #     result_data = read_standalone_table(table_path, field_names, where_clause)

# #     # Process and use the data as needed
# #     if result_data:
# #         for row in result_data:
# #             print(row[0])  # Print each row of data


# import arcpy


# def get_attribute_names(table_path):
#     # Use a try-except block to handle any potential errors
#     try:
#         # Get a list of field objects from the table
#         fields = arcpy.ListFields(table_path)

#         # Extract the names of the attributes (fields) from the field objects
#         attribute_names = [field.name for field in fields]

#         return attribute_names

#     except arcpy.ExecuteError as e:
#         print("Error occurred: ", e)
#         return None


# if __name__ == "__main__":
#     # Example usage:
#     arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb" # Set your workspace here
#     # Change to the name of your standalone table or feature class
#     table_path = "land_parcel"

#     # Call the function to get attribute names from the table
#     result_attribute_names = get_attribute_names(table_path)

#     # Process and use the attribute names as needed
#     if result_attribute_names:
#         for name in result_attribute_names:
#             print(name)  # Print each attribute name

# field_name = ["SHAPE@", "proposal_id", "business_name", "company_name", "company_code", "plant_code", "state", "site", "district", "tehshil", "village", "survey_no", "parcel_area",
#               "land_type", "seller_name", "acquired_status", "sale_deed_status", "mutation_status", "na_status", "tsr_status", "free_hold_area", "lease_area", "used_area", "unused_area"]
# a = [tuple(field_name)]

# print(len(field_name))
# print(a)

# for x in range(2, 24):
#     print(x)


# LaRe--83586
# 1
# 1
# ADSF
# ADSF
# HIMACHAL PRADESH
# Ahmedabad
# ADSF
# ADSF
# SHIMLA
# 123
# 333
# government
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF
# ADSF


# "Proposal ID", "BusinessName", "CompanyName","CompanyCode", "PlantCode","State Code", "Site Code","District Code", "Tehshil Code","Village Code", "Survey No","parcel Area Code", "Land Type","Seller Name", "Acquired Status","Sale Deed Status", "Mutation Status","NA Status","TSR Status", "Free Hold Area", "Lease Area","Used Area", "Unused Area"


# attributes = ["Proposal ID", "BusinessName", "CompanyName", "CompanyCode", "PlantCode", "State Code", "Site Code", "District Code", "Tehshil Code", "Village Code", "Survey No",
#               "parcel Area Code", "Land Type", "Seller Name", "Acquired Status", "Sale Deed Status", "Mutation Status", "NA Status", "TSR Status", "Free Hold Area", "Lease Area", "Used Area", "Unused Area"]
# field_name = ["SHAPE@", "field_no", "business_name", "company_name", "company_code", "plant_code", "state", "site", "district", "tehshil", "village", "survey_no", "parcel_area",
#               "land_type", "seller_name", "acquired_status", "sale_deed_status", "mutation_status", "na_status", "tsr_status", "free_hold_area", "lease_area", "used_area", "unused_area"]

# print(len(attributes))
# print(len(field_name))


import arcpy
import re

# arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb"
# fieldList = arcpy.ListFields(
#     r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.shp")
src_shp = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\sample_land_info.shp"
fieldList = arcpy.ListFields(src_shp)
# Loop through each field in the list and print the name
for field in fieldList:
    print('"' + field.name + '",')
    # if field.name not in ["FID", "Shape", "OBJECTID", "geometry", "id", "field_id", "field_no", "request_id", "proposal_id"]:
    # arcpy.AddField_management(src_shp, field.name, "TEXT")

# src_shp = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\sample_land_info.shp"
# field_name = ["SHAPE@", "field_no", "business_name", "company_name"]
# attributes = ["", "Proposal ID", "BusinessName", "CompanyName"]

# with arcpy.da.InsertCursor("land_parcels", field_name) as iCursor:
#     with arcpy.da.SearchCursor(src_shp, ["SHAPE@"]) as sCursor:
#         for row in sCursor:
#             print(row)
#             attributes[0] = row[0]
#             iCursor.insertRow(tuple(attributes))
