import bpy
from .interface import ui_panel


@ui_panel
class LOGIC_NODES_PT_project_management(bpy.types.Panel):
    bl_idname = "LOGIC_NODES_PT_project_management"
    bl_label = "Project Management"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
        
        layout = self.layout
        layout.prop(prefs, 'project_path')
        
        c = layout.column()
        c.enabled = prefs.project_path != ''
        r = c.row()
        r.prop(prefs, 'copy_engine')
        r.prop(prefs, 'use_symlink')

        c.operator('logic_nodes.generate_project')
