from .menus import *  # Importing all menu components from the menus module.

# Function to add a property menu for the MustardUI.
def mustardui_property_menuadd(self, context):
    # Calls a helper function to get the active object in the context.
    res, obj = mustardui_active_object(context, config=1)

    # Check if the context has 'button_prop' attribute and if an object was found.
    if hasattr(context, 'button_prop') and res:
        # Retrieve settings from the current scene and rig settings from the selected object.
        settings = bpy.context.scene.MustardUI_Settings
        rig_settings = obj.MustardUI_RigSettings

        layout = self.layout  # Get the layout for the UI.

        # Add a separator in the UI for better organization.
        layout.separator()

        # Initialize an operator for adding properties in the UI.
        op = layout.operator(MustardUI_Property_MenuAdd.bl_idname)
        op.section = ""
        op.outfit = ""
        op.outfit_piece = ""
        op.hair = ""

        sep = False  # A flag for managing the layout, not used further in this code.

        # Loop through all outfit collections in the rig settings.
        for collection in [x for x in rig_settings.outfits_collections if x.collection is not None]:
            # Choose which objects to display based on rig settings.
            items = collection.collection.all_objects if rig_settings.outfit_config_subcollections else collection.collection.objects
            
            # Loop through each object in the items.
            for object in [x for x in items]:
                # Check if the object is the currently selected active object.
                if object == context.active_object:
                    # Create an operator to add the current outfit piece.
                    op = layout.operator(MustardUI_Property_MenuAdd.bl_idname,
                                         text="Add to " + context.active_object.name, icon="MOD_CLOTH")
                    op.section = ""
                    op.outfit = collection.collection.name  # Set outfit name.
                    op.outfit_piece = object.name  # Set outfit piece name.
                    op.hair = ""  # Reset hair attribute.
                    break  # Exit once the active object is found.

        # Check for extras collection in rig settings, handling it similarly as above.
        if rig_settings.extras_collection is not None:
            items = rig_settings.extras_collection.all_objects if rig_settings.outfit_config_subcollections else rig_settings.extras_collection.objects
            if len(items) > 0:  # If there are items in the extras collection.
                for object in [x for x in items]:
                    if object == context.active_object:  # Check if it's the active object.
                        op = layout.operator(MustardUI_Property_MenuAdd.bl_idname,
                                             text="Add to " + context.active_object.name, icon="PLUS")
                        op.section = ""
                        op.outfit = rig_settings.extras_collection.name  # Set outfit name.
                        op.outfit_piece = object.name  # Set outfit piece name.
                        op.hair = ""  # Reset hair attribute.
                        break  # Exit once the active object is found.

        # Check the hair collection similarly, ensuring it contains MESH object types.
        if rig_settings.hair_collection is not None:
            if len(rig_settings.hair_collection.objects) > 0:
                for object in [x for x in rig_settings.hair_collection.objects if x.type == "MESH"]:
                    if object == context.active_object:  # Check if it's the active object.
                        op = layout.operator(MustardUI_Property_MenuAdd.bl_idname,
                                             text="Add to " + context.active_object.name, icon="STRANDS")
                        op.section = ""
                        op.outfit = ""  # Reset outfit name.
                        op.outfit_piece = ""  # Reset outfit piece name.
                        op.hair = object.name  # Set hair name.
                        break  # Exit once the active object is found.

        layout.separator()  # Add another separator for better layout organization.

        # If there are body custom properties, add a menu for them.
        if len(rig_settings.body_custom_properties_sections) > 0:
            layout.menu(OUTLINER_MT_MustardUI_PropertySectionMenu.bl_idname)
        
        # If there are outfit collections, add a menu for outfits.
        if len([x for x in rig_settings.outfits_collections if x.collection is not None]) > 0:
            layout.menu(OUTLINER_MT_MustardUI_PropertyOutfitMenu.bl_idname, icon="MOD_CLOTH")
        
        # If there are hair collection objects, add a hair menu.
        if rig_settings.hair_collection is not None:
            if len(rig_settings.hair_collection.objects) > 0:
                layout.menu(OUTLINER_MT_MustardUI_PropertyHairMenu.bl_idname, icon="STRANDS")


# Function to link a property in the MustardUI.
def mustardui_property_link(self, context):
    # Calls a helper function to get the active object in the context.
    res, obj = mustardui_active_object(context, config=1)

    # Check if the context has 'button_prop' attribute and if an object was found.
    if hasattr(context, 'button_prop') and res:
        layout = self.layout  # Get the layout for the UI.
        # Add a menu for linking properties in the UI.
        self.layout.menu(MUSTARDUI_MT_Property_LinkMenu.bl_idname, icon="LINKED")
