# -*- coding: utf-8 -*-

import arcpy

attribute_value = None


class ShpLoader():
    def __init__(self, src_shp, attributes) -> None:
        self.src_shp = src_shp
        self.attributes = attributes
        # self.attributes.insert(0, "")
        self.field_name = ["field_no", "business_name", "company_name", "state", "site", "district", "tehshil", "company_code", "plant_code", "village", "survey_no", "parcel_area",
                           "land_type", "seller_name", "acquired_status", "sale_deed_status", "mutation_status", "na_status", "tsr_status", "free_hold_area", "lease_area", "used_area", "unused_area", "SHAPE@"]
        arcpy.AddMessage(str(len(self.attributes)))
        arcpy.AddMessage(str(len(self.field_name)))

    @staticmethod
    def read_standalone_table(table_path, field_names, where_clause) -> None:
        # Create a list to store the data
        data = []

        # Use a try-except block to handle any potential errors
        try:
            # Open a search cursor to read the data from the standalone table
            with arcpy.da.SearchCursor(table_path, field_names, where_clause) as cursor:
                for row in cursor:
                    # Process each row and store the data
                    data.append(row)

        except arcpy.ExecuteError as e:
            print("Error occurred: ", e)
            return None

        return data

    def updateLandParcel(self):
        # result_data = read_standalone_table(table_path, field_names, where_clause)

        with arcpy.da.InsertCursor("land_parcels", self.field_name) as iCursor:
            with arcpy.da.SearchCursor(self.src_shp, ["village", "survey_no", "parcel_are", "land_type", "seller_nam", "acquired_s", "sale_deed_", "mutation_s", "na_status", "tsr_status", "free_hold_", "lease_area", "used_area", "unused_are", "SHAPE@"]) as sCursor:
                for row in sCursor:

                    arcpy.AddMessage("Attribute Length" +
                                     str(len(self.attributes)))
                    arcpy.AddMessage("row Length" + str(len(row)))
                    arcpy.AddMessage(str(len(self.attributes + list(row))))
                    iCursor.insertRow(tuple(self.attributes + list(row)))
                    # iCursor.insertRow([row[0], self.attributes])
        # if arcpy.Exists("temp_lyr"):
        #     arcpy.Delete_management("temp_lyr")


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "LAMSToolBox"
        self.alias = "LAMSToolBox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Land Parcel Update"
        self.description = ""
        self.canRunInBackground = False
        arcpy.env.workspace = r"C:\Stuff\DR-AKSHAY\LAMS\DATA\LandParcel\LandParcel\LandParcel.gdb"

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Parameter 1
        in_proposal_id = arcpy.Parameter(
            name='proposalID',
            displayName='Proposal ID',
            datatype='String',
            direction='Input',
            parameterType='Required')
        # Parameter 2
        in_business_name = arcpy.Parameter(
            name='businessName',
            displayName='Business Name',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')
        # Parameter 3
        in_company_name = arcpy.Parameter(
            name='companyName',
            displayName='Company Name',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')
        # in_company_name.enabled = False

        # Parameter 4
        in_state = arcpy.Parameter(
            name='stateCode',
            displayName='State',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        # Parameter 5
        in_site = arcpy.Parameter(
            name='siteCode',
            displayName='Site',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        # Parameter 6
        in_district = arcpy.Parameter(
            name='districtCode',
            displayName='District',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        # Parameter 7
        in_tehshil = arcpy.Parameter(
            name='tehshilCode',
            displayName='Tehshil',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        # Parameter 8
        in_company_code = arcpy.Parameter(
            name='companyCode',
            displayName='Company Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')
        in_company_code.filter.list = ['Category A', 'Category B']

        # Parameter 9
        in_plant_code = arcpy.Parameter(
            name='plantCode',
            displayName='Plant Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')
        in_plant_code.filter.list = [
            'Plant Code A', 'Plant Code B', 'Plant Code D']

        # Reference Land Parcel layer
        # ## Parameter 0
        in_land_parcel = arcpy.Parameter(
            displayName="Land Parcel Shape File",
            name="landParcelShape",
            datatype="DEShapefile",
            parameterType="Required",
            enabled=True,
            direction="Input")

        return [in_land_parcel, in_proposal_id, in_business_name, in_company_name,
                in_state, in_site, in_district, in_tehshil,  in_company_code, in_plant_code]
        # return [in_proposal_id, in_business_name, in_company_name]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value:
            for x in range(2, 10):
                parameters[x].enabled = True
            sql_query = "request_id='{}'".format(parameters[1].value)

            with arcpy.da.SearchCursor("request", ["business_unit", "company", "state_id", "location", "district_id", "city_id"], sql_query) as rows:
                for row in rows:
                    parameters[2].value = ShpLoader.read_standalone_table(
                        table_path="business_unit", field_names="name", where_clause="id={}".format(row[0]))[0][0]  # in_business_name
                    parameters[3].value = ShpLoader.read_standalone_table(
                        table_path="company", field_names="name", where_clause="id={}".format(row[1]))[0][0]  # in_company_name

                    parameters[4].value = ShpLoader.read_standalone_table(
                        table_path="state", field_names="state_name", where_clause="id={}".format(row[2]))[0][0]  # in_state
                    parameters[5].value = row[3]  # in_site
                    parameters[6].value = ShpLoader.read_standalone_table(
                        table_path="district", field_names="district_name", where_clause="id={}".format(row[4]))[0][0]  # in_district
                    parameters[7].value = ShpLoader.read_standalone_table(
                        table_path="city", field_names="city", where_clause="id={}".format(row[5]))[0][0]  # tehshil
                    global attribute_value
                    attribute_value = list(row).copy()
                    attribute_value.insert(0, parameters[1].value)

        else:
            for x in range(2, 10):
                parameters[x].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inFeatures = parameters[0].valueAsText
        arcpy.AddMessage(len(attribute_value))
        params_list = attribute_value
        for x in range(8, 10):
            arcpy.AddMessage(parameters[x].valueAsText)
            params_list.append(parameters[x].valueAsText)

        shp_loader = ShpLoader(src_shp=inFeatures, attributes=params_list)
        shp_loader.updateLandParcel()

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
