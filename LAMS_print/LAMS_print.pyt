# -*- coding: utf-8 -*-

import arcpy, os

class Status():
    YES = 'YES'
    NO  = 'NO'

class CreatePrintLayout:
    def __init__(self, site_name, business_name):
        """Define the layout and setting the title etc."""
        self.project_path     = r"C:\Stuff\DR-AKSHAY\NEW\LAMS\Toolbox\DATA\Lams_print.aprx"
        self.input_fc         = os.path.join(r"C:\Stuff\DR-AKSHAY\NEW\LAMS\DATA\Hoshiyarpur_LAMS\Hoshiyarpur_LAMS.gdb" ,"Hoshiarpur_wgs84")
        self.layout_name      = "LAMS"
        self.site_name        = site_name
        self.attribute_field  = "Site"
        self.business_name    = business_name

        self.XMin  = 0
        self.YMin  = 0
        self.XMax  = 0
        self.YMax  = 0

        self.land_id_count   = 0
        self.sale_deed_count = 0
        self.mutation_count  = 0
        self.na_count        = 0

        self.fields          = ["SaleDeedStatus", "MutationStatus", "NA_Status"]

        uuid                 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_path     = os.path.join(arcpy.env.scratchFolder, "{}_{}_{}".format(site_name, business_name, uuid))
       # Create a SQL expression to query features
        self.sql_expression  = "{} = '{}'".format(arcpy.AddFieldDelimiters(self.input_fc, self.attribute_field), site_name)

    def getSiteExtent(self):
        # Use a search cursor to query features matching the attribute value
        cursor = arcpy.da.SearchCursor(self.input_fc, ["SHAPE@"], where_clause=self.sql_expression)

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
            arcpy.AddMessage("Combined Extent: " + str(combined_extent.XMin) + str(combined_extent.YMin) + str(combined_extent.XMax) + str(combined_extent.YMax))
            return combined_extent
        else:
            arcpy.AddMessage("No features found matching the attribute value.")
        # self.Xmin = combined_extent.XMin
        # self.YMin = combined_extent.YMin
        # self.XMax = combined_extent.XMax
        # self.YMax = combined_extent.YMax




    def getLandStatus(self):
        # Create a search cursor to iterate through the data
        with arcpy.da.SearchCursor(self.input_fc, self.fields) as cursor:
            for row in cursor:
                # Extract values from each row
                sale_deed_value = row[0]
                mutation_value = row[1]
                na_value = row[2]

                if sale_deed_value == Status.NO:
                    self.land_id_count = self.land_id_count + 1
                elif na_value == Status.YES:
                    self.na_count = self.na_count + 1
                elif sale_deed_value == Status.YES and mutation_value == Status.NO:
                    self.sale_deed_count = self.sale_deed_count + 1
                elif mutation_value == Status.YES and na_value == Status.NO:
                    self.mutation_count = self.mutation_count + 1


    def setMapLayout(self):
        # Open the project
        project = arcpy.mp.ArcGISProject(self.project_path)

        # Get the desired layout
        layout = project.listLayouts(self.layout_name)[0]

        # Add a map frame to the layout
        map_frame = layout.listElements("MAPFRAME_ELEMENT", "MapLayout")[0]
        spatial_extent = self.getSiteExtent()
        arcpy.AddMessage("Combined Extent: " + str(spatial_extent.XMin) + str(spatial_extent.YMin) + str(spatial_extent.XMax) + str(spatial_extent.YMax))
        map_frame.camera.setExtent(spatial_extent)
        arcpy.AddMessage(map_frame.getLayerExtent(project.listMaps()[0].listLayers()[0]))
        project.save()
        # 76.06290613000004, 31.311182320000057, 76.07161014400003, 31.3177167400000
        # spatial_extent = arcpy.Extent(76.06290613000004, 31.311182320000057, 76.07161014400003, 31.3177167400000)
        # map_frame.camera.setExtent(spatial_extent)
        # map_frame.camera.setExtent(spatial_extent)
        # map_frame.camera.setExtent(map_frame.getLayerExtent(project.listMaps()[0].listLayers()[0]))

        site_business = layout.listElements("TEXT_ELEMENT", "Title")[0]
        site_business.text = str(site_business.text).replace("[[site]]", self.site_name).replace("[[business]]", self.business_name)

        land_status = layout.listElements("TEXT_ELEMENT", "LandStatus")[0]
        land_status.text = str(land_status.text).replace("[[landIdentified]]", str(self.land_id_count)).replace("[[sale_deed]]", str(self.sale_deed_count)).replace("[[mutation]]", str(self.mutation_count)).replace("[[na]]", str(self.na_count))

        legend = layout.listElements("LEGEND_ELEMENT")[0]
        legend.autoAdd = True

        layout.exportToPDF(self.output_path)

        # Clean up
        del project


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "MAP-PRINT"
        self.alias = "MAP-PRINT"

        # List of tool classes associated with this toolbox
        self.tools = [MapPrint]


class MapPrint:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "MAP-PRINT"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
                # Parameter 0: Site Name
        param_site_name = arcpy.Parameter(
            displayName   = "Site Name",
            name          = "site_name",
            datatype      = "String",
            parameterType = "Required",
            direction     = "Input"
        )

        # Parameter 1: Business Unit
        param_business_unit = arcpy.Parameter(
            displayName   = "Business Unit",
            name          = "business_unit",
            datatype      = "String",
            parameterType = "Required",
            direction     = "Input"
        )
        return [param_site_name, param_business_unit]

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
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Get the parameters
        site_name     = parameters[0].valueAsText
        business_unit = parameters[1].valueAsText

        mp_layout = CreatePrintLayout(site_name, business_unit)
        mp_layout.getLandStatus()
        mp_layout.setMapLayout()
        arcpy.AddMessage("Return file is " + mp_layout.output_path)
        arcpy.SetParameter(1, mp_layout.output_path)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
