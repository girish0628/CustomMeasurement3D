# -*- coding: utf-8 -*-

import arcpy, datetime, os

path_toSDE = r"C:\Stuff\DR-AKSHAY\NEW\LAMS\APRX\LandParcelExport\LandParcelExport.gdb"
land_fc = "landparcel"


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
        arcpy.CopyFeatures_management(in_features=in_feature_class, out_feature_class=output_land_fc)
        try:
            if arcpy.Describe(path_toSDE).dataType != "Workspace":
                raise
            arcpy.CopyFeatures_management(in_features=in_feature_class, out_feature_class=output_land_fc)
        except:
            arcpy.AddError("SDE path '{}' is not correct".format(in_feature_class))
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
