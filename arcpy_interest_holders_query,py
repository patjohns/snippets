# Class method to return tenure interest holders using arcpy make query layer

def get_interest_holder(self, file_number, disposition_id) -> str:
        # If primary client desired, add clause: AND tt.PRIMARY_CONTACT_YRN = 'Y'
        # Note that sql comments (--) cannot be used in sql_query passed to MakeQueryLayer()

        sql_query = f"""
            SELECT
                tcts.OBJECTID, 
                tcts.SHAPE, 
                LEGAL_NAME, 
                FIRST_NAME, 
                LAST_NAME

            FROM WHSE_TANTALIS.TA_CROWN_TENURES_SVW tcts
                JOIN WHSE_TANTALIS.TA_TENANTS tt
                    ON tcts.DISPOSITION_TRANSACTION_SID = tt.DISPOSITION_TRANSACTION_SID
                        AND tt.SEPARATION_DAT IS null
                JOIN WHSE_TANTALIS.TA_INTERESTED_PARTIES tip
                    ON tt.INTERESTED_PARTY_SID = tip.INTERESTED_PARTY_SID

            WHERE 
                tcts.CROWN_LANDS_FILE = '{file_number}' AND tcts.DISPOSITION_TRANSACTION_SID = {disposition_id}
            """
        query_lyr = 'query_lyr'
        arcpy.management.MakeQueryLayer(
                        input_database=self.bcgw, 
                        out_layer_name=query_lyr, 
                        query=sql_query, 
                        oid_fields="OBJECTID", 
                        shape_type="POLYGON", 
                        srid=3005
                        )
        
        # Set to ensure unique values
        str_tenure_interest_holders = set()
 
        with arcpy.da.SearchCursor(query_lyr, ['LEGAL_NAME', 'LAST_NAME', 'FIRST_NAME']) as s_cursor:
            for row in s_cursor:
                if row[0] is not None: # Default to organization name
                    str_tenure_interest_holders.add(row[0])
                else:
                    name = f'{row[1]}, {row[2]}'
                    str_tenure_interest_holders.add(name)
        
        arcpy.management.Delete(query_lyr)   
        
        # Semicolon delimiter b/c of commas b/w LAST_NAME FIRST_NAME
        out_string = '; '.join(str_tenure_interest_holders)

        return out_string
