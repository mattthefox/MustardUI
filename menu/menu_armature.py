import bpy

from bpy import props
from . import MainPanel
from ..model_selection.active_object import *
from ..warnings.ops_fix_old_UI import check_old_UI
from ..settings.rig import *

class PANEL_PT_MustardUI_Armature(MainPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_MustardUI_Armature"
    bl_label = "Armature"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_armature_button(self, armature, bcoll, bcoll_settings, bcolls, armature_settings, layout):

        def draw_with_icon(armature, prop, prop_name, name, icon):
            subrow = row.row(align=True)
            # icon comes first which is for visibility.
            if icon != "NONE":
                subrow.prop(prop, prop_name,
                         text="",
                         toggle=True,
                         icon=icon)
            else:
                subrow.prop(prop, prop_name,
                         text="",
                         toggle=True,
                         icon="DOT")
            return subrow
                

        if not armature_settings.mirror:
            row = layout.row()
            subrow = draw_with_icon(armature, bcoll, "is_visible", bcoll.name, bcoll_settings.icon)
            select_op = subrow.operator("armature.select_bones_from_collection",text=bcoll.name)
            select_op.bcoll = bcoll.name;
            select_op.the_armature = armature.name
            subrow.prop(bcoll,"is_solo",text="",icon="SOLO_OFF",toggle=True)
            return

        for b in bcolls:
            if (
                    bcoll.name.lower().endswith(".l") and b.name.lower() == bcoll.name[:-2].lower() + ".r"
            ) or (
                    bcoll.name.lower().startswith("left") and b.name.lower() == "right" + bcoll.name[4:].lower()
            ):
                row = layout.row()
                subrow = draw_with_icon(armature, bcoll, "is_visible", bcoll.name, bcoll_settings.icon)
                select_op = subrow.operator("armature.select_bones_from_collection",text=bcoll.name)
                select_op.bcoll = bcoll.name;
                select_op.the_armature = armature.name
                subrow.prop(bcoll,"is_solo",text="",icon="SOLO_OFF",toggle=True)

                r_icon = b.MustardUI_ArmatureBoneCollection.icon
                subrow = draw_with_icon(armature, b, "is_visible", b.name, r_icon)
                select_opR = subrow.operator("armature.select_bones_from_collection",text=b.name)
                select_opR.bcoll = b.name;
                select_opR.the_armature = armature.name
                subrow.prop(b,"is_solo",text="",icon="SOLO_OFF",toggle=True)
                return
            elif (
                    bcoll.name.lower().endswith(".r") and b.name.lower() == bcoll.name[:-2].lower() + ".l"
            ) or (
                    bcoll.name.lower().startswith("right") and b.name.lower() == "left" + bcoll.name[5:].lower()
            ):
                return

        row = layout.row()
        subrow = draw_with_icon(armature, bcoll, "is_visible", bcoll.name, bcoll_settings.icon)
        select_op = subrow.operator("armature.select_bones_from_collection",text=bcoll.name)
        select_op.bcoll = bcoll.name;
        select_op.the_armature = armature.name
        subrow.prop(bcoll,"is_solo",text="",icon="SOLO_OFF",toggle=True)

    @classmethod
    def poll(cls, context):

        if check_old_UI():
            return False

        res, obj = mustardui_active_object(context, config=0)

        if obj is not None:
            rig_settings = obj.MustardUI_RigSettings
            armature_settings = obj.MustardUI_ArmatureSettings
            bcolls = obj.collections_all if bpy.app.version >= (4, 1, 0) else obj.collections

            if len(bcolls) < 1:
                return False

            enabled_colls = [x for x in bcolls if x.MustardUI_ArmatureBoneCollection.is_in_UI]

            if rig_settings.hair_collection is not None:
                return res and (len(enabled_colls) > 0 or (len([x for x in rig_settings.hair_collection.objects if
                                                                x.type == "ARMATURE"]) > 1 and armature_settings.enable_automatic_hair))
            else:
                return res and len(enabled_colls) > 0
        else:
            return res

    def draw(self, context):

        settings = bpy.context.scene.MustardUI_Settings
        poll, obj = mustardui_active_object(context, config=0)
        armature_settings = obj.MustardUI_ArmatureSettings
        rig_settings = obj.MustardUI_RigSettings


        bcolls = obj.collections_all if bpy.app.version >= (4, 1, 0) else obj.collections

        box = self.layout

        draw_separator = False
        if rig_settings.hair_collection is not None and armature_settings.enable_automatic_hair:
            if len([x for x in rig_settings.hair_collection.objects if x.type == "ARMATURE"]) > 0:
                box.prop(armature_settings, "hair", toggle=True, icon="CURVES")
                draw_separator = True

        if len(rig_settings.outfits_list) > 0:
            if len([x for x in bcolls if x.MustardUI_ArmatureBoneCollection.outfit_switcher_enable]):
                box.prop(armature_settings, "outfits", toggle=True, icon="MOD_CLOTH")
                draw_separator = True

        if draw_separator:
            box.separator()

        enabled_colls = [x for x in bcolls if x.MustardUI_ArmatureBoneCollection.is_in_UI]

        box.use_property_split = False
        box.use_property_decorate = True  # No animation.

        for bcoll in enabled_colls:
            bcoll_settings = bcoll.MustardUI_ArmatureBoneCollection
            if (bcoll_settings.advanced and settings.advanced) or not bcoll_settings.advanced:
                self.draw_armature_button(obj, bcoll, bcoll_settings, enabled_colls, armature_settings, box)

class SelectBonesFromCollection(bpy.types.Operator):
    bl_idname = "armature.select_bones_from_collection"
    bl_label = "Select Bones from Collection"
    bl_description = "Select all bones in the specified bone collection"
    bl_options = {'REGISTER', 'UNDO'}

    # Bone collection property
    bcoll: bpy.props.StringProperty()
    the_armature: bpy.props.StringProperty()

    def execute(self, context):
        if self.bcoll is not None:
            armature = bpy.data.armatures[self.the_armature]
            bone_names = [bone.name for bone in armature.bones if bone.name in armature.collections[self.bcoll].bones]
            
            # Deselect all bones first
            for bone in armature.bones:
                bone.select = False
            
            # Select the bones found in the specified collection
            for bone_name in bone_names:
                armature.bones[bone_name].select = True

            return {'FINISHED'}
        
        return {'CANCELLED'}

def register():
    bpy.utils.register_class(SelectBonesFromCollection)
    bpy.utils.register_class(PANEL_PT_MustardUI_Armature)


def unregister():
    bpy.utils.unregister_class(PANEL_PT_MustardUI_Armature)
    bpy.utils.unregister_class(SelectBonesFromCollection)
