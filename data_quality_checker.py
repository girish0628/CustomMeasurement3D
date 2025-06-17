import arcpy
import os
from collections import defaultdict

def comprehensive_data_quality_check(shapefile_path, rainfall_table_path, output_gdb):
    """
    Perform comprehensive data quality checks on input data
    
    Args:
        shapefile_path (str): Path to state shapefile
        rainfall_table_path (str): Path to rainfall table in FGDB
        output_gdb (str): Path to output geodatabase for reports
    """
    
    try:
        print("=== Comprehensive Data Quality Check ===")
        
        # Create quality report table
        quality_report_table = os.path.join(output_gdb, "Data_Quality_Report")
        
        if not arcpy.Exists(output_gdb):
            gdb_path = os.path.dirname(output_gdb)
            gdb_name = os.path.basename(output_gdb)
            arcpy.management.CreateFileGDB(gdb_path, gdb_name)
        
        # Create quality report table structure
        arcpy.management.CreateTable(output_gdb, "Data_Quality_Report")
        arcpy.management.AddField(quality_report_table, "CHECK_TYPE", "TEXT", field_length=100)
        arcpy.management.AddField(quality_report_table, "DATASET", "TEXT", field_length=100)
        arcpy.management.AddField(quality_report_table, "STATUS", "TEXT", field_length=50)
        arcpy.management.AddField(quality_report_table, "DETAILS", "TEXT", field_length=500)
        arcpy.management.AddField(quality_report_table, "RECORD_COUNT", "LONG")
        
        quality_issues = []
        
        # Check 1: Verify datasets exist
        print("Checking dataset existence...")
        if not arcpy.Exists(shapefile_path):
            quality_issues.append(("Dataset Existence", "Shapefile", "FAIL", f"File not found: {shapefile_path}", 0))
        else:
            shp_count = int(arcpy.management.GetCount(shapefile_path).getOutput(0))
            quality_issues.append(("Dataset Existence", "Shapefile", "PASS", f"File exists with {shp_count} records", shp_count))
        
        if not arcpy.Exists(rainfall_table_path):
            quality_issues.append(("Dataset Existence", "Rainfall Table", "FAIL", f"Table not found: {rainfall_table_path}", 0))
        else:
            table_count = int(arcpy.management.GetCount(rainfall_table_path).getOutput(0))
            quality_issues.append(("Dataset Existence", "Rainfall Table", "PASS", f"Table exists with {table_count} records", table_count))
        
        # Check 2: Field validation
        print("Checking field structure...")
        
        # Shapefile fields
        if arcpy.Exists(shapefile_path):
            shp_fields = [f.name for f in arcpy.ListFields(shapefile_path)]
            if 'state_name' in [f.lower() for f in shp_fields]:
                quality_issues.append(("Field Structure", "Shapefile", "PASS", "state_name field found", len(shp_fields)))
            else:
                quality_issues.append(("Field Structure", "Shapefile", "FAIL", f"state_name field missing. Available: {shp_fields}", len(shp_fields)))
        
        # Table fields
        if arcpy.Exists(rainfall_table_path):
            table_fields = [f.name for f in arcpy.ListFields(rainfall_table_path)]
            if 'state_name' in [f.lower() for f in table_fields]:
                quality_issues.append(("Field Structure", "Rainfall Table", "PASS", "state_name field found", len(table_fields)))
            else:
                quality_issues.append(("Field Structure", "Rainfall Table", "FAIL", f"state_name field missing. Available: {table_fields}", len(table_fields)))
        
        # Check 3: Geometry validation
        print("Checking geometry...")
        if arcpy.Exists(shapefile_path):
            # Check for invalid geometries
            temp_layer = "temp_geometry_check"
            arcpy.management.MakeFeatureLayer(shapefile_path, temp_layer)
            
            # Select invalid geometries
            arcpy.management.SelectLayerByAttribute(temp_layer, "NEW_SELECTION", "Shape_Area IS NULL OR Shape_Area <= 0")
            invalid_count = int(arcpy.management.GetCount(temp_layer).getOutput(0))
            
            if invalid_count == 0:
                quality_issues.append(("Geometry Validation", "Shapefile", "PASS", "All geometries are valid", 0))
            else:
                quality_issues.append(("Geometry Validation", "Shapefile", "WARNING", f"{invalid_count} invalid geometries found", invalid_count))
            
            arcpy.management.Delete(temp_layer)
        
        # Check 4: Data completeness
        print("Checking data completeness...")
        
        # Check for null/empty state names in shapefile
        if arcpy.Exists(shapefile_path):
            null_states_shp = 0
            with arcpy.da.SearchCursor(shapefile_path, ["state_name"]) as cursor:
                for row in cursor:
                    if not row[0] or row[0].strip() == '':
                        null_states_shp += 1
            
            if null_states_shp == 0:
                quality_issues.append(("Data Completeness", "Shapefile", "PASS", "No null state names", 0))
            else:
                quality_issues.append(("Data Completeness", "Shapefile", "WARNING", f"{null_states_shp} null/empty state names", null_states_shp))
        
        # Check for null/empty state names in table
        if arcpy.Exists(rainfall_table_path):
            null_states_table = 0
            with arcpy.da.SearchCursor(rainfall_table_path, ["state_name"]) as cursor:
                for row in cursor:
                    if not row[0] or row[0].strip() == '':
                        null_states_table += 1
            
            if null_states_table == 0:
                quality_issues.append(("Data Completeness", "Rainfall Table", "PASS", "No null state names", 0))
            else:
                quality_issues.append(("Data Completeness", "Rainfall Table", "WARNING", f"{null_states_table} null/empty state names", null_states_table))
        
        # Check 5: State name matching
        print("Checking state name matching...")
        if arcpy.Exists(shapefile_path) and arcpy.Exists(rainfall_table_path):
            # Get unique state names
            shp_states = set()
            with arcpy.da.SearchCursor(shapefile_path, ["state_name"]) as cursor:
                for row in cursor:
                    if row[0] and row[0].strip():
                        shp_states.add(row[0].strip().lower())
            
            table_states = set()
            with arcpy.da.SearchCursor(rainfall_table_path, ["state_name"]) as cursor:
                for row in cursor:
                    if row[0] and row[0].strip():
                        table_states.add(row[0].strip().lower())
            
            matched_states = shp_states & table_states
            unmatched_shp = shp_states - table_states
            unmatched_table = table_states - shp_states
            
            match_percentage = (len(matched_states) / max(len(shp_states), len(table_states))) * 100
            
            if match_percentage >= 90:
                status = "PASS"
            elif match_percentage >= 70:
                status = "WARNING"
            else:
                status = "FAIL"
            
            details = f"Match rate: {match_percentage:.1f}%. Matched: {len(matched_states)}, Unmatched in shapefile: {len(unmatched_shp)}, Unmatched in table: {len(unmatched_table)}"
            quality_issues.append(("State Name Matching", "Both Datasets", status, details, len(matched_states)))
        
        # Insert quality issues into report table
        print("Generating quality report...")
        with arcpy.da.InsertCursor(quality_report_table, ["CHECK_TYPE", "DATASET", "STATUS", "DETAILS", "RECORD_COUNT"]) as cursor:
            for issue in quality_issues:
                cursor.insertRow(issue)
        
        # Print summary
        print("\n=== Data Quality Summary ===")
        pass_count = sum(1 for issue in quality_issues if issue[2] == "PASS")
        warning_count = sum(1 for issue in quality_issues if issue[2] == "WARNING")
        fail_count = sum(1 for issue in quality_issues if issue[2] == "FAIL")
        
        print(f"Total checks: {len(quality_issues)}")
        print(f"Passed: {pass_count}")
        print(f"Warnings: {warning_count}")
        print(f"Failed: {fail_count}")
        
        if fail_count == 0:
            print("✓ Data quality is acceptable for processing")
        else:
            print("✗ Critical issues found - please review before processing")
        
        print(f"\nDetailed report saved to: {quality_report_table}")
        
        return fail_count == 0
        
    except Exception as e:
        print(f"Error in data quality check: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    # Define paths - UPDATE THESE
    shapefile_path = r"C:\path\to\your\india_states.shp"
    rainfall_table_path = r"C:\path\to\your\data.gdb\rainfall_data"
    output_gdb = r"C:\path\to\output\Quality_Reports.gdb"
    
    print("=== Data Quality Checker ===")
    print(f"Shapefile: {shapefile_path}")
    print(f"Rainfall Table: {rainfall_table_path}")
    print(f"Output GDB: {output_gdb}")
    print("=" * 50)
    
    # Run quality check
    quality_passed = comprehensive_data_quality_check(
        shapefile_path=shapefile_path,
        rainfall_table_path=rainfall_table_path,
        output_gdb=output_gdb
    )
    
    if quality_passed:
        print("\n✓ All quality checks passed - ready for centroid generation!")
    else:
        print("\n✗ Quality issues detected - please review the report before proceeding")
