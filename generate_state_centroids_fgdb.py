import arcpy
import os
from arcpy import env

def generate_state_centroids_fgdb(input_shapefile, rainfall_table, output_gdb, centroid_fc_name="State_Centroids"):
    """
    Generate centroid points for each state from shapefile and store in FGDB
    
    Args:
        input_shapefile (str): Path to the input shapefile containing state polygons
        rainfall_table (str): Path to the rainfall table in FGDB
        output_gdb (str): Path to output geodatabase
        centroid_fc_name (str): Name for the output centroid feature class
    """
    
    try:
        # Set environment settings
        env.overwriteOutput = True
        
        print("Starting centroid generation process...")
        print(f"Input Shapefile: {input_shapefile}")
        print(f"Rainfall Table: {rainfall_table}")
        print(f"Output GDB: {output_gdb}")
        
        # Create output geodatabase if it doesn't exist
        if not arcpy.Exists(output_gdb):
            gdb_path = os.path.dirname(output_gdb)
            gdb_name = os.path.basename(output_gdb)
            arcpy.management.CreateFileGDB(gdb_path, gdb_name)
            print(f"Created geodatabase: {output_gdb}")
        
        # Full path to output centroid feature class
        output_centroids = os.path.join(output_gdb, centroid_fc_name)
        
        # Step 1: Generate centroid points using Feature To Point tool
        print("Generating centroid points from state polygons...")
        arcpy.management.FeatureToPoint(
            in_features=input_shapefile,
            out_feature_class=output_centroids,
            point_location="CENTROID"
        )
        
        # Get count of generated centroids
        centroid_count = int(arcpy.management.GetCount(output_centroids).getOutput(0))
        print(f"Generated {centroid_count} centroid points")
        
        # Step 2: Add coordinate fields to store X,Y values
        print("Adding coordinate fields...")
        arcpy.management.AddField(output_centroids, "CENTROID_X", "DOUBLE", field_alias="Centroid X")
        arcpy.management.AddField(output_centroids, "CENTROID_Y", "DOUBLE", field_alias="Centroid Y")
        
        # Step 3: Calculate coordinate values
        print("Calculating coordinate values...")
        arcpy.management.CalculateGeometryAttributes(
            in_features=output_centroids,
            geometry_property=[["CENTROID_X", "POINT_X"], ["CENTROID_Y", "POINT_Y"]],
            coordinate_system=arcpy.Describe(output_centroids).spatialReference
        )
        
        # Step 4: Join with rainfall data
        print("Joining centroid data with rainfall table...")
        joined_fc_name = f"{centroid_fc_name}_with_Rainfall"
        joined_fc = os.path.join(output_gdb, joined_fc_name)
        
        # Perform the join
        arcpy.management.JoinField(
            in_data=output_centroids,
            in_field="state_name",
            join_table=rainfall_table,
            join_field="state_name"
        )
        
        # Copy the joined feature class to preserve the join
        arcpy.management.CopyFeatures(output_centroids, joined_fc)
        
        print(f"Successfully created joined feature class: {joined_fc}")
        
        # Get final count
        final_count = int(arcpy.management.GetCount(joined_fc).getOutput(0))
        print(f"Final feature class contains {final_count} records")
        
        # Step 5: Create summary report
        create_summary_report(joined_fc, output_gdb)
        
        return joined_fc
        
    except arcpy.ExecuteError:
        print("ArcPy Error:")
        print(arcpy.GetMessages(2))
        return None
    except Exception as e:
        print(f"General Error: {str(e)}")
        return None

def create_summary_report(feature_class, output_gdb):
    """
    Create a summary report table with centroid information
    
    Args:
        feature_class (str): Path to the feature class with centroids and rainfall data
        output_gdb (str): Path to output geodatabase
    """
    
    try:
        print("Creating summary report...")
        
        # Create summary table
        summary_table = os.path.join(output_gdb, "Centroid_Summary_Report")
        
        # Get field information
        fields = arcpy.ListFields(feature_class)
        field_info = []
        
        # Prepare fields for cursor
        cursor_fields = ["state_name", "CENTROID_X", "CENTROID_Y"]
        
        # Add rainfall-related fields
        for field in fields:
            if any(keyword in field.name.lower() for keyword in ['rainfall', 'precipitation', 'rain']):
                cursor_fields.append(field.name)
                field_info.append(field.name)
        
        # Create summary table structure
        arcpy.management.CreateTable(output_gdb, "Centroid_Summary_Report")
        
        # Add fields to summary table
        arcpy.management.AddField(summary_table, "STATE_NAME", "TEXT", field_length=100)
        arcpy.management.AddField(summary_table, "CENTROID_LONGITUDE", "DOUBLE")
        arcpy.management.AddField(summary_table, "CENTROID_LATITUDE", "DOUBLE")
        arcpy.management.AddField(summary_table, "RAINFALL_RECORDS", "LONG")
        arcpy.management.AddField(summary_table, "DATA_STATUS", "TEXT", field_length=50)
        
        # Insert summary data
        insert_fields = ["STATE_NAME", "CENTROID_LONGITUDE", "CENTROID_LATITUDE", "RAINFALL_RECORDS", "DATA_STATUS"]
        
        with arcpy.da.InsertCursor(summary_table, insert_fields) as insert_cursor:
            with arcpy.da.SearchCursor(feature_class, cursor_fields) as search_cursor:
                for row in search_cursor:
                    state_name = row[0]
                    centroid_x = row[1]
                    centroid_y = row[2]
                    
                    # Count non-null rainfall values
                    rainfall_count = sum(1 for val in row[3:] if val is not None and val != '')
                    
                    # Determine data status
                    if rainfall_count > 0:
                        data_status = "Complete"
                    else:
                        data_status = "Missing Rainfall Data"
                    
                    # Insert summary record
                    insert_cursor.insertRow([state_name, centroid_x, centroid_y, rainfall_count, data_status])
        
        print(f"Summary report created: {summary_table}")
        
    except Exception as e:
        print(f"Error creating summary report: {str(e)}")

def validate_fgdb_data(shapefile_path, rainfall_table_path):
    """
    Validate data in shapefile and FGDB table
    
    Args:
        shapefile_path (str): Path to shapefile
        rainfall_table_path (str): Path to rainfall table in FGDB
    """
    
    try:
        print("=== Data Validation Report ===")
        
        # Validate shapefile
        if not arcpy.Exists(shapefile_path):
            print(f"ERROR: Shapefile not found: {shapefile_path}")
            return False
        
        shp_count = int(arcpy.management.GetCount(shapefile_path).getOutput(0))
        print(f"Shapefile records: {shp_count}")
        
        # Check for state_name field in shapefile
        shp_fields = [f.name.lower() for f in arcpy.ListFields(shapefile_path)]
        if 'state_name' not in shp_fields:
            print("ERROR: 'state_name' field not found in shapefile")
            print(f"Available fields: {[f.name for f in arcpy.ListFields(shapefile_path)]}")
            return False
        
        # Validate rainfall table
        if not arcpy.Exists(rainfall_table_path):
            print(f"ERROR: Rainfall table not found: {rainfall_table_path}")
            return False
        
        table_count = int(arcpy.management.GetCount(rainfall_table_path).getOutput(0))
        print(f"Rainfall table records: {table_count}")
        
        # Check for state_name field in table
        table_fields = [f.name.lower() for f in arcpy.ListFields(rainfall_table_path)]
        if 'state_name' not in table_fields:
            print("ERROR: 'state_name' field not found in rainfall table")
            print(f"Available fields: {[f.name for f in arcpy.ListFields(rainfall_table_path)]}")
            return False
        
        # Get unique state names from both datasets
        print("\nComparing state names...")
        
        # Get state names from shapefile
        shp_states = set()
        with arcpy.da.SearchCursor(shapefile_path, ["state_name"]) as cursor:
            for row in cursor:
                if row[0]:
                    shp_states.add(row[0].strip().lower())
        
        # Get state names from table
        table_states = set()
        with arcpy.da.SearchCursor(rainfall_table_path, ["state_name"]) as cursor:
            for row in cursor:
                if row[0]:
                    table_states.add(row[0].strip().lower())
        
        # Compare state names
        matched_states = shp_states & table_states
        shp_only = shp_states - table_states
        table_only = table_states - shp_states
        
        print(f"Unique states in shapefile: {len(shp_states)}")
        print(f"Unique states in table: {len(table_states)}")
        print(f"Matched states: {len(matched_states)}")
        
        if shp_only:
            print(f"\nStates in shapefile only ({len(shp_only)}):")
            for state in sorted(shp_only):
                print(f"  - {state}")
        
        if table_only:
            print(f"\nStates in table only ({len(table_only)}):")
            for state in sorted(table_only):
                print(f"  - {state}")
        
        print("\n=== Validation Complete ===")
        return len(matched_states) > 0
        
    except Exception as e:
        print(f"Validation Error: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    # Define file paths - UPDATE THESE PATHS
    input_shapefile = r"C:\Stuff\RAIN\india_states.shp"
    rainfall_table = r"C:\Stuff\RAIN\rain_analaytics.gdb\sub_division"  # Table in FGDB
    output_geodatabase = r"C:\path\to\output\IndiaStates_Analysis.gdb"
    
    print("=== State Centroid Generation from FGDB ===")
    print(f"Input Shapefile: {input_shapefile}")
    print(f"Rainfall Table: {rainfall_table}")
    print(f"Output GDB: {output_geodatabase}")
    print("=" * 60)
    
    # Step 1: Validate input data
    if validate_fgdb_data(input_shapefile, rainfall_table):
        print("\nData validation passed. Proceeding with centroid generation...")
        
        # Step 2: Generate centroids and join with rainfall data
        result_fc = generate_state_centroids_fgdb(
            input_shapefile=input_shapefile,
            rainfall_table=rainfall_table,
            output_gdb=output_geodatabase,
            centroid_fc_name="State_Centroids"
        )
        
        if result_fc:
            print("\n" + "=" * 60)
            print("Process completed successfully!")
            print(f"Output feature class: {result_fc}")
            print(f"Summary report: {os.path.join(output_geodatabase, 'Centroid_Summary_Report')}")
        else:
            print("Failed to generate centroids.")
    else:
        print("Data validation failed. Please check your input data.")
