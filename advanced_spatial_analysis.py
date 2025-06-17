import arcpy
import os
from arcpy import env

def create_rainfall_analysis_features(centroid_fc, output_gdb):
    """
    Create additional spatial analysis features for rainfall data
    
    Args:
        centroid_fc (str): Path to centroid feature class with rainfall data
        output_gdb (str): Path to output geodatabase
    """
    
    try:
        print("Creating advanced spatial analysis features...")
        
        # Set environment
        env.overwriteOutput = True
        
        # 1. Create Thiessen Polygons for rainfall interpolation
        print("Creating Thiessen polygons...")
        thiessen_fc = os.path.join(output_gdb, "Rainfall_Thiessen_Polygons")
        
        arcpy.analysis.CreateThiessenPolygons(
            in_features=centroid_fc,
            out_feature_class=thiessen_fc,
            fields_to_copy="ALL"
        )
        
        # 2. Create buffer zones around centroids
        print("Creating buffer zones...")
        buffer_fc = os.path.join(output_gdb, "State_Centroid_Buffers")
        
        # Create 50km buffer zones
        arcpy.analysis.Buffer(
            in_features=centroid_fc,
            out_feature_class=buffer_fc,
            buffer_distance_or_field="50 Kilometers",
            line_side="FULL",
            line_end_type="ROUND",
            dissolve_option="NONE"
        )
        
        # 3. Create near table for closest state analysis
        print("Creating near table for spatial relationships...")
        near_table = os.path.join(output_gdb, "State_Proximity_Analysis")
        
        arcpy.analysis.GenerateNearTable(
            in_features=centroid_fc,
            near_features=centroid_fc,
            out_table=near_table,
            search_radius="500 Kilometers",
            location="LOCATION",
            angle="ANGLE",
            closest="ALL"
        )
        
        # 4. Create rainfall statistics table
        create_rainfall_statistics(centroid_fc, output_gdb)
        
        print("Advanced spatial analysis features created successfully!")
        
        return {
            'thiessen': thiessen_fc,
            'buffers': buffer_fc,
            'near_table': near_table
        }
        
    except Exception as e:
        print(f"Error in advanced spatial analysis: {str(e)}")
        return None

def create_rainfall_statistics(centroid_fc, output_gdb):
    """
    Create statistical analysis of rainfall data
    
    Args:
        centroid_fc (str): Path to centroid feature class with rainfall data
        output_gdb (str): Path to output geodatabase
    """
    
    try:
        print("Creating rainfall statistics...")
        
        # Create statistics table
        stats_table = os.path.join(output_gdb, "Rainfall_Statistics")
        
        # Get rainfall fields
        fields = arcpy.ListFields(centroid_fc)
        rainfall_fields = []
        
        for field in fields:
            if any(keyword in field.name.lower() for keyword in ['rainfall', 'precipitation', 'rain']):
                if field.type in ['Double', 'Float', 'Integer', 'SmallInteger']:
                    rainfall_fields.append(field.name)
        
        if rainfall_fields:
            # Create summary statistics
            stats_fields = []
            for field in rainfall_fields:
                stats_fields.extend([
                    [field, "MEAN"],
                    [field, "MAX"],
                    [field, "MIN"],
                    [field, "STD"]
                ])
            
            arcpy.analysis.Statistics(
                in_table=centroid_fc,
                out_table=stats_table,
                statistics_fields=stats_fields,
                case_field="state_name"
            )
            
            print(f"Rainfall statistics created: {stats_table}")
        else:
            print("No rainfall fields found for statistical analysis")
            
    except Exception as e:
        print(f"Error creating rainfall statistics: {str(e)}")

def export_to_formats(feature_class, output_folder):
    """
    Export feature class to various formats
    
    Args:
        feature_class (str): Path to input feature class
        output_folder (str): Path to output folder
    """
    
    try:
        print("Exporting to various formats...")
        
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Get base name
        base_name = os.path.basename(feature_class)
        
        # 1. Export to Shapefile
        print("Exporting to Shapefile...")
        shp_output = os.path.join(output_folder, f"{base_name}.shp")
        arcpy.conversion.FeatureClassToFeatureClass(
            in_features=feature_class,
            out_path=output_folder,
            out_name=f"{base_name}.shp"
        )
        
        # 2. Export to KML
        print("Exporting to KML...")
        kml_output = os.path.join(output_folder, f"{base_name}.kml")
        arcpy.conversion.LayerToKML(
            layer=feature_class,
            out_kmz_file=kml_output
        )
        
        # 3. Export to Excel
        print("Exporting to Excel...")
        excel_output = os.path.join(output_folder, f"{base_name}.xlsx")
        arcpy.conversion.TableToExcel(
            Input_Table=feature_class,
            Output_Excel_File=excel_output
        )
        
        print(f"Exports completed in: {output_folder}")
        
        return {
            'shapefile': shp_output,
            'kml': kml_output,
            'excel': excel_output
        }
        
    except Exception as e:
        print(f"Error during export: {str(e)}")
        return None

# Main execution for advanced analysis
if __name__ == "__main__":
    # Define paths - UPDATE THESE
    input_centroid_fc = r"C:\Stuff\RAIN\IndiaStates_Analysis.gdb\sub_division"
    output_gdb = r"C:\Stuff\RAIN\IndiaStates_Analysis.gdb"
    export_folder = r"C:\Stuff\RAIN"
    
    print("=== Advanced Spatial Analysis ===")
    print(f"Input Feature Class: {input_centroid_fc}")
    print(f"Output GDB: {output_gdb}")
    print("=" * 50)
    
    # Run advanced analysis
    analysis_results = create_rainfall_analysis_features(input_centroid_fc, output_gdb)
    
    if analysis_results:
        print("\nAdvanced analysis completed!")
        
        # Export to various formats
        export_results = export_to_formats(input_centroid_fc, export_folder)
        
        if export_results:
            print("\nExport completed!")
            print("Files created:")
            for format_type, file_path in export_results.items():
                print(f"  - {format_type.upper()}: {file_path}")
