import bpy
from . import MainPanel
from ..model_selection.active_object import *
from ..warnings.ops_fix_old_UI import check_old_UI
from ..settings.rig import *


class PANEL_PT_MustardUI_SelectModel(MainPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_MustardUI_SelectModel"
    bl_label = "Model Selection"

    @classmethod
    def poll(cls, context):
        if check_old_UI():
            return False

        settings = bpy.context.scene.MustardUI_Settings
        res, arm = mustardui_active_object(context, config=0)
        return res and len(
            [x for x in bpy.data.armatures if x.MustardUI_created]) > 1 and not settings.viewport_model_selection

    def draw(self, context):
        settings = bpy.context.scene.MustardUI_Settings

        layout = self.layout
 
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                if obj.data.MustardUI_created:
                    rig_settings = obj.data.MustardUI_RigSettings
                    row = layout.row(align=True)
                    if rig_settings.model_collection:
                        row.prop(rig_settings.model_collection, "hide_viewport",text="",icon="OUTLINER_COLLECTION",invert_checkbox=True)
                    row.prop(obj, "hide_viewport",text="",icon="OUTLINER_OB_ARMATURE", invert_checkbox=True)
                    row.operator('mustardui.switchmodel', text=obj.data.MustardUI_RigSettings.model_name,
                                    depress=obj.data == settings.panel_model_selection_armature).model_to_switch = obj.data.name

    """
        for armature in [x for x in bpy.data.armatures if x.MustardUI_created]:
            row = layout.row(align=True)
            row.prop()
            row.operator('mustardui.switchmodel', text=armature.MustardUI_RigSettings.model_name,
                            depress=armature == settings.panel_model_selection_armature).model_to_switch = armature.name
    """

def register():
    bpy.utils.register_class(PANEL_PT_MustardUI_SelectModel)


def unregister():
    bpy.utils.unregister_class(PANEL_PT_MustardUI_SelectModel)
