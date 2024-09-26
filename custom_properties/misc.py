import bpy


# Function to check keys of custom properties (only for debug)
def dump(obj, text):
    print('-' * 40, text, '-' * 40)
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


# Function to check over all custom properties
def mustardui_check_cp(obj, rna, path):
    for cp in obj.MustardUI_CustomProperties:
        if cp.rna == rna and cp.path == path:
            return False

    for cp in obj.MustardUI_CustomPropertiesOutfit:
        if cp.rna == rna and cp.path == path:
            return False

    for cp in obj.MustardUI_CustomPropertiesHair:
        if cp.rna == rna and cp.path == path:
            return False

    return True


# Function to choose correct custom properties list
def mustardui_choose_cp(obj, type, scene):
    if type == "BODY":
        return obj.MustardUI_CustomProperties, scene.mustardui_property_uilist_index
    elif type == "OUTFIT":
        return obj.MustardUI_CustomPropertiesOutfit, scene.mustardui_property_uilist_outfits_index
    else:
        return obj.MustardUI_CustomPropertiesHair, scene.mustardui_property_uilist_hair_index


def mustardui_update_index_cp(type, scene, index):
    if type == "BODY":
        scene.mustardui_property_uilist_index = index
    elif type == "OUTFIT":
        scene.mustardui_property_uilist_outfits_index = index
    else:
        scene.mustardui_property_uilist_hair_index = index


import bpy

def mustardui_add_driver(obj, rna, path, prop, prop_name):
    # Assuming the bone name is "Props"
    bone_name = "mui_props"
    armature = obj  # Assuming obj is the armature

    # Check if the bone exists
    if bone_name not in armature.data.bones:
        # Create the bone if it doesn't exist
        bpy.ops.object.mode_set(mode='EDIT')  # Switch to edit mode
        new_bone = armature.data.edit_bones.new(bone_name)  # Create a new bone
        new_bone.head = (0, 0, 0)  # Set the head position (customize as needed)
        new_bone.tail = (0, 0, 1)  # Set the tail position (customize as needed)
        bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode

    # Proceed with the driver setup
    driver_object = eval(rna)
    driver_object.driver_remove(path)
    driver = driver_object.driver_add(path)

    # Set the data path to access the custom properties of the "Props" bone
    bone_data_path = f'pose.bones["{bone_name}"]["{prop_name}"]'

    # No array property
    if prop.array_length == 0:
        driver = driver.driver
        driver.type = "AVERAGE"
        var = driver.variables.new()
        var.name = 'mustardui_var'
        var.targets[0].id_type = "ARMATURE"
        var.targets[0].id = obj
        var.targets[0].data_path = bone_data_path

    # Array property
    else:
        for i in range(prop.array_length):
            driver[i] = driver[i].driver
            driver[i].type = "AVERAGE"

            var = driver[i].variables.new()
            var.name = 'mustardui_var'
            var.targets[0].id_type = "ARMATURE"
            var.targets[0].id = obj
            var.targets[0].data_path = f'{bone_data_path}[{i}]'  # Target the array within the bone's properties

    return




def mustardui_clean_prop(obj, uilist, index, addon_prefs):
    # Assuming the bone name is "Props"
    bone_name = "Props"
    
    # Clear UI Data from the Props bone's custom properties
    try:
        ui_data = obj.pose.bones[bone_name].id_properties_ui(uilist[index].prop_name)
        ui_data.clear()
    except:
        if addon_prefs.debug:
            print('MustardUI - Could not clear UI properties. Skipping for this custom property')

    # Delete custom property from the Props bone
    try:
        del obj.pose.bones[bone_name][uilist[index].prop_name]
    except:
        if addon_prefs.debug:
            print('MustardUI - Properties not found. Skipping custom properties deletion')

    # ... (rest of the function remains unchanged)



def mustardui_cp_path(rna, path):
    return rna + "." + path if not all(["[" in path, "]" in path]) else rna + path
