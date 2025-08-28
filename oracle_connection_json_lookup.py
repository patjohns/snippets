def get_staff_info(self, json_file, sde) -> None:
        """
        Class method to use Oracle SDE connection to get info from json lookup via username
        """
        
        # Get the Oracle username from the BCGW connection properties
        desc = arcpy.Describe(sde)
        oracle_username = desc.connectionProperties.user
        
        try:
            # Load the JSON file
            with open(json_file, "r") as file:
                staff_info = json.load(file)

            # Retrieve staff details based on the Oracle username
            staff_details = staff_info.get(oracle_username, {
                "name": "Unknown",
                "title": "Unknown",
                "email": "Unknown",
                "phone": "Unknown"
            })

            # Set the LandsFileInfo object attributes
            self.staff_contact_name = staff_details["name"]
            self.staff_contact_title = staff_details["title"]
            self.staff_contact_email = staff_details["email"]
            self.staff_contact_phone = staff_details["phone"]

        except Exception as e:
            self.logger.error(f"Failed to retrieve staff contact information: {str(e)}")
            # Set default values in case of an error
            self.staff_contact_name = "Unknown"
            self.staff_contact_title = "Unknown"
            self.staff_contact_email = "Unknown"
            self.staff_contact_phone = "Unknown"
