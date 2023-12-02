import bpy
from bpy.props import *
from .. import bl_info


class MustardUI_Updater(bpy.types.Operator):
    """Check MustardUI version"""
    bl_idname = "mustardui.updater"
    bl_label = "Check Version"
    bl_options = {'UNDO'}

    v = [0, 0, 0, 0]

    def __init__(self):
        self.data = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        version = (self.v[0], self.v[1], self.v[2])

        if bl_info["version"] >= version:
            self.report({'INFO'}, "MustardUI: The current version is already up-to-date")
        else:
            bpy.ops.mustardui.openlink(url="github.com/Mustard2/MustardUI/releases/latest")

        return {'FINISHED'}

    def invoke(self, context, event):

        import requests

        # Import the data from the GitHub repository file
        try:
            response = requests.get("https://raw.githubusercontent.com/Mustard2/MustardUI/master/__init__.py")
            self.data = response.text
        except:
            self.report({'ERROR'}, "MustardUI: Error while retrieving remote version. Check your connection")
            return {'FINISHED'}

        # Fetch version
        if '"version": (' in self.data:
            find = self.data.split('"version": (', 1)[1]
            self.v[0] = int(find.split(',')[0])
            self.v[1] = int(find.split(',')[1])
            self.v[2] = int(find.split(',')[2])
            self.v[3] = find.split(',')[3]
            self.v[3] = int(self.v[3].split(')')[0])
        else:
            self.report({'ERROR'}, "MustardUI: Can not find the version number of the remote repository")
            return {'FINISHED'}

        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):

        layout = self.layout

        version = (self.v[0], self.v[1], self.v[2])

        box = layout.box()

        if bl_info["version"] > version:
            box.label(text="The current version seems up-to-date.", icon="INFO")
        else:
            box.label(text="Update available!", icon="INFO")

        row = box.row()
        row.label(text="Current version: ", icon="RIGHTARROW_THIN")
        row.label(text=str(bl_info["version"][0]) + '.' + str(bl_info["version"][1]) + '.' + str(
            bl_info["version"][2]) + '.' + str(bl_info["version"][3]))
        row = box.row()
        row.label(text="Remote version: ", icon="WORLD")
        row.label(
            text=str(self.v[0]) + '.' + str(self.v[1]) + '.' + str(self.v[2]) + '.' + str(self.v[3]))

        if bl_info["version"] < version:
            box = layout.box()
            box.label(text="Click 'OK' to open the latest release page.", icon="ERROR")


def register():
    bpy.utils.register_class(MustardUI_Updater)


def unregister():
    bpy.utils.unregister_class(MustardUI_Updater)