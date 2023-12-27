# -*- coding: utf-8 -*-

import arcpy, datetime, os
import json

path_toSDE = r"C:\Stuff\DR-AKSHAY\NEW\LAMS\APRX\LandParcelExport\LandParcelExport.gdb"
land_fc = "landparcel"



json_data = '''
{
  "items": [
    {
      "name"     : "BusinessName",
      "temp_name": "BusinessName_1",
      "table"    : "business_unit",
      "field"    : "name"
    },
    {
      "name"     : "CompanyName",
      "temp_name": "CompanyName_1",
      "table"    : "company",
      "field"    : "name"
    },
    {
      "name"     : "State",
      "temp_name": "State_1",
      "table"    : "state",
      "field"    : "state_name"
    },
    {
      "name"     : "District",
      "temp_name": "District_1",
      "table"    : "district",
      "field"    : "district_name"
    }
  ]
}
'''


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Land Parcel Exporter Toolbox"
        self.alias = "LPExporterToolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Exporter]


class Exporter:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Exporter"
        self.description = "Land Parcel Exporter Toolbox"

    def getParameterInfo(self):
        """Define the tool parameters."""
        OutputPath = arcpy.Parameter(
            displayName="Output Geodatabase",
            name="out_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
            )
        params = [OutputPath]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        gdb_path = parameters[0].valueAsText
        if ".gdb" not in gdb_path:
            parameters[0].setErrorMessage("{0} is not the correct path of FGDB.".format(gdb_path))
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_feature_class = os.path.join(path_toSDE, land_fc)
        gdb_path = parameters[0].valueAsText
        output_land_fc_name = "land_parcel_{}".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        output_land_fc = os.path.join(gdb_path, output_land_fc_name)

        try:
            if arcpy.Describe(path_toSDE).dataType != "Workspace":
                raise
            arcpy.CopyFeatures_management(in_features=in_feature_class, out_feature_class=output_land_fc)

            data = json.loads(json_data)
            for item in data['items']:
                # field_name = "{}_1".format(field)
                old_field_name = "$feature.{}".format(item['name'])
                joined_table = os.path.join(path_toSDE, item['table'])
                # Run AddField twice for two new fields
                arcpy.AddField_management(output_land_fc, item['temp_name'], "LONG", 0,
                                field_alias=item['temp_name'], field_is_nullable="NULLABLE")

                arcpy.CalculateField_management(output_land_fc, item['temp_name'], old_field_name, "ARCADE")
                arcpy.JoinField_management(output_land_fc, item['temp_name'], joined_table, "id", [item['field']])
                if arcpy.Exists("{}_i01xx0".format(output_land_fc_name)):
                    arcpy.Delete_management("{}_i01xx0".format(output_land_fc_name))

                arcpy.DeleteField_management(output_land_fc, [item['name'], item['temp_name']])

                arcpy.AlterField_management(output_land_fc, item['field'], item['name'], item['name'])

        except:
            arcpy.AddError("SDE path '{}' is not correct".format(in_feature_class))
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
