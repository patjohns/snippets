import arcpy

def select_true_overlaps(input_features, selecting_features):
    """
    Selects features from input_features that truly overlap select_features,
    meaning that adjacent features are NOT selected (as with ArcPy intersect selection relationship)

    Parameters:
        input_features: Input features to be selected (str)
        select_features: Selecting features (str)

    Note: Be aware of which relationships the methods (contains, overlaps, within) apply to (e.g., line to line)

    Returns:
        List of ObjectIDs (list)
    """
    # Ensure input_features is a layer prior to selection
    if not arcpy.Describe(input_features).dataType == "FeatureLayer":
        input_layer = "input_features_layer"
        arcpy.management.MakeFeatureLayer(input_features, input_layer)
    else:
        input_layer = input_features

    # Perform initial select by location (intersect)
    arcpy.management.SelectLayerByLocation(
        in_layer=input_layer,
        overlap_type="INTERSECT",
        select_features=selecting_features,
        selection_type="NEW_SELECTION"
        )
    
    # List to store ObjectIDs of overlapping features
    overlapping_oids = []

    with arcpy.da.SearchCursor(input_layer, ["SHAPE@", "OID@"]) as target_cursor:
        for target_row in target_cursor:
            target_geom = target_row[0]  # Target geometry
            if target_geom is None:
                continue  # Skip features with no geometry

            is_overlapping = False

            with arcpy.da.SearchCursor(selecting_features, ["SHAPE@"]) as join_cursor:
                for join_row in join_cursor:
                    join_geom = join_row[0]  # Join geometry

                    if (target_geom.overlaps(join_geom) or # Check overlaps (overlaps/contains/within)
                        target_geom.contains(join_geom) or 
                        target_geom.within(join_geom)):
                        is_overlapping = True

                    # If overlapping, no need to continue checking
                    if is_overlapping:
                        break

            # If the feature overlaps, add it to list
            if is_overlapping:
                overlapping_oids.append(target_row[1])

    # Clear selection on input_layer
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=input_layer,
        selection_type="CLEAR_SELECTION"
        )
    
    # Return ObjectIDs of overlapping features
    return overlapping_oids
