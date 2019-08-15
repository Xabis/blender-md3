bl_info = {
    "name": "Quake 3 Model (.md3)",
    "author": "Vitaly Verhovodov",
    "version": (0, 2, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export > Quake 3 Model",
    "description": "Quake 3 Model format (.md3)",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/MD3",
    "tracker_url": "https://github.com/neumond/blender-md3/issues",
    "category": "Import-Export",
}

#Reload submodules when the main script is reloaded
if "bpy" in locals():
    import importlib
    if "export_md3" in locals():
        print("Reloading: export_md3")
        importlib.reload(export_md3)
    if "import_md3" in locals():
        print("Reloading: import_md3")
        importlib.reload(import_md3)

import bpy
import struct
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


class ImportMD3(bpy.types.Operator, ImportHelper):
    '''Import a Quake 3 Model MD3 file'''
    bl_idname = "import_scene.md3"
    bl_label = 'Import MD3'
    filename_ext = ".md3"
    filter_glob = StringProperty(default="*.md3", options={'HIDDEN'})

    def execute(self, context):
        from .import_md3 import MD3Importer
        MD3Importer(context)(self.properties.filepath)
        return {'FINISHED'}


class ExportMD3(bpy.types.Operator, ExportHelper):
    '''Export a Quake 3 Model MD3 file'''
    bl_idname = "export_scene.md3"
    bl_label = 'Export MD3'
    filename_ext = ".md3"
    filter_glob = StringProperty(default="*.md3", options={'HIDDEN'})

    def execute(self, context):
        try:
            from .export_md3 import MD3Exporter
            MD3Exporter(context)(self.properties.filepath)
            return {'FINISHED'}
        except struct.error:
            self.report({'ERROR'}, "Mesh does not fit within the MD3 model space. Vertex axies locations must be below 512 blender units.")
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'CANCELLED'}


def menu_func_import(self, context):
    self.layout.operator(ImportMD3.bl_idname, text="Quake 3 Model (.md3)")


def menu_func_export(self, context):
    self.layout.operator(ExportMD3.bl_idname, text="Quake 3 Model (.md3)")

classes = (
    ImportMD3,
    ExportMD3
)

# Taken from https://github.com/CGCookie/blender-addon-updater
def make_annotations(cls):
    """Converts class fields to annotations if running with Blender 2.8"""
    if bpy.app.version < (2, 80):
        return cls
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls

def get_import_menu():
    if hasattr(bpy.types, "TOPBAR_MT_file_import"):
        return bpy.types.TOPBAR_MT_file_import      #2.8
    return bpy.types.INFO_MT_file_import            #2.7

def get_export_menu():
    if hasattr(bpy.types, "TOPBAR_MT_file_export"):
        return bpy.types.TOPBAR_MT_file_export      #2.8
    return bpy.types.INFO_MT_file_export            #2.7

def register():
    for cls in classes:
        make_annotations(cls)
        bpy.utils.register_class(cls)

    get_import_menu().append(menu_func_import)
    get_export_menu().append(menu_func_export)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    get_import_menu().remove(menu_func_import)
    get_export_menu().remove(menu_func_export)

if __name__ == "__main__":
    register()
