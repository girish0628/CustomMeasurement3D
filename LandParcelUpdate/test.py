# import arcpy


# def read_standalone_table(table_path, field_names, where_clause):
#     # Create a list to store the data
#     data = []

#     # Use a try-except block to handle any potential errors
#     try:
#         # Open a search cursor to read the data from the standalone table
#         with arcpy.da.SearchCursor(table_path, field_names, where_clause) as cursor:
#             for row in cursor:
#                 # Process each row and store the data
#                 data.append(row)

#     except arcpy.ExecuteError as e:
#         print("Error occurred: ", e)
#         return None

#     return data


# if __name__ == "__main__":
#     # Example usage:
#     arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb"
#     table_path = "state"  # Change to the name of your standalone table
#     # Replace with the field names you want to read
#     field_names = ["state_name"]
#     where_clause = "id=1"

#     # Call the function to read data from the standalone table
#     result_data = read_standalone_table(table_path, field_names, where_clause)

#     # Process and use the data as needed
#     if result_data:
#         for row in result_data:
#             print(row[0])  # Print each row of data


import arcpy


def get_attribute_names(table_path):
    # Use a try-except block to handle any potential errors
    try:
        # Get a list of field objects from the table
        fields = arcpy.ListFields(table_path)

        # Extract the names of the attributes (fields) from the field objects
        attribute_names = [field.name for field in fields]

        return attribute_names

    except arcpy.ExecuteError as e:
        print("Error occurred: ", e)
        return None


if __name__ == "__main__":
    # Example usage:
    arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb" # Set your workspace here
    # Change to the name of your standalone table or feature class
    table_path = "land_parcel"

    # Call the function to get attribute names from the table
    result_attribute_names = get_attribute_names(table_path)

    # Process and use the attribute names as needed
    if result_attribute_names:
        for name in result_attribute_names:
            print(name)  # Print each attribute name
