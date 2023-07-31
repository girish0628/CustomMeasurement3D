# -*- coding: utf-8 -*-

import arcpy


class ShpLoader():
    def __init__(self, src_shp, attributes) -> None:
        self.src_shp = src_shp
        self.attributes = attributes
        self.field_name = ["SHAPE@", "proposal_id", "business_name", "company_name", "company_code", "plant_code", "state", "site", "district", "tehshil", "village", "survey_no", "parcel_area",
                           "land_type", "seller_name", "acquired_status", "sale_deed_status", "mutation_status", "na_status", "tsr_status", "free_hold_area", "lease_area", "used_area", "unused_area"]

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

        with arcpy.da.InsertCursor("land_parcel", self.field_name) as iCursor:
            with arcpy.da.SearchCursor(self.src_shp, ["SHAPE@"]) as sCursor:
                for row in sCursor:
                    self.attributes.insert(0, row[0])
                    iCursor.insertRow(self.attributes)
                    # iCursor.insertRow([row[0], aValue])
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

        in_proposal_id = arcpy.Parameter(
            name='proposalID',
            displayName='Proposal ID',
            datatype='String',
            direction='Input',
            parameterType='Required')

        in_business_name = arcpy.Parameter(
            name='businessName',
            displayName='Business Name',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_company_name = arcpy.Parameter(
            name='companyName',
            displayName='Company Name',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')
        # in_company_name.enabled = False

        in_company_code = arcpy.Parameter(
            name='companyCode',
            displayName='Company Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_plant_code = arcpy.Parameter(
            name='plantCode',
            displayName='Plant Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_state = arcpy.Parameter(
            name='stateCode',
            displayName='State Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_site = arcpy.Parameter(
            name='siteCode',
            displayName='Site Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_district = arcpy.Parameter(
            name='districtCode',
            displayName='District Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_tehshil = arcpy.Parameter(
            name='tehshilCode',
            displayName='Tehshil Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_village = arcpy.Parameter(
            name='villageCode',
            displayName='Village Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_survey_no = arcpy.Parameter(
            name='surveyNo',
            displayName='Survey No',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_parcel_area = arcpy.Parameter(
            name='parcelAreaCode',
            displayName='parcel Area Code',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_land_type = arcpy.Parameter(
            name='landType',
            displayName='Land Type',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_seller_name = arcpy.Parameter(
            name='sellerName',
            displayName='Seller Name',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_acquired_status = arcpy.Parameter(
            name='acquiredStatus',
            displayName='Acquired Status',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_sale_deed_status = arcpy.Parameter(
            name='saleDeedStatus',
            displayName='Sale Deed Status',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_mutation_status = arcpy.Parameter(
            name='mutationStatus',
            displayName='Mutation Status',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_na_status = arcpy.Parameter(
            name='naStatus',
            displayName='NA Status',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_tsr_status = arcpy.Parameter(
            name='tsrStatus',
            displayName='TSR Status',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_free_hold_area = arcpy.Parameter(
            name='freeHoldArea',
            displayName='Free Hold Area',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_lease_area = arcpy.Parameter(
            name='leaseArea',
            displayName='Lease Area',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_used_area = arcpy.Parameter(
            name='usedArea',
            displayName='Used Area',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        in_unused_area = arcpy.Parameter(
            name='unusedArea',
            displayName='Unused Area',
            datatype='String',
            direction='Input',
            enabled=False,
            parameterType='Required')

        # Reference Land Parcel layer
        in_land_parcel = arcpy.Parameter(
            displayName="Land Parcel Shape File",
            name="landParcelShape",
            datatype="DEShapefile",
            parameterType="Required",
            enabled=False,
            direction="Input")

        return [in_proposal_id, in_land_parcel, in_business_name, in_company_name,
                in_company_code, in_plant_code, in_state, in_site,
                in_district, in_tehshil, in_village, in_survey_no,
                in_parcel_area, in_land_type, in_seller_name,
                in_acquired_status, in_sale_deed_status, in_mutation_status,
                in_na_status, in_tsr_status, in_free_hold_area, in_lease_area,
                in_used_area, in_unused_area]
        # return [in_proposal_id, in_business_name, in_company_name]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].value:
            for x in range(1, 23):
                parameters[x].enabled = True
            sql_query = "request_id='{}'".format(parameters[0].value)
            with arcpy.da.SearchCursor("request", ["business_unit", "company", "village", "land_type", "state_id", "location", "district_id"], sql_query) as rows:
                for row in rows:
                    parameters[2].value = row[0]  # in_business_name
                    parameters[3].value = row[1]  # in_company_name
                    parameters[10].value = row[2]
                    parameters[13].value = row[3]

                    parameters[6].value = ShpLoader.read_standalone_table(
                        table_path="state", field_names="state_name", where_clause="id={}".format(row[4]))[0][0]  # in_state
                    parameters[7].value = row[5]  # in_site
                    parameters[10].value = ShpLoader.read_standalone_table(
                        table_path="district", field_names="district_name", where_clause="id={}".format(row[6]))[0][0]  # in_district
        else:
            for x in range(1, 23):
                parameters[x].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inFeatures = parameters[1].valueAsText
        params_list = []
        for x in range(2, 23):
            params_list.append(parameters[x].valueAsText)

        shp_loader = ShpLoader(src_shp=inFeatures, attributes=params_list)
        shp_loader.updateLandParcel()

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
