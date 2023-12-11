import bpy
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree
from ..utilities import preferences


@ui_panel
class LOGIC_NODES_PT_help(bpy.types.Panel):
    bl_label = "Help & Documentation"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Help & Documentation"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.3
        
        box = layout.box()
        box.operator(
            "logic_nodes.open_upbge_docs",
            text="Engine API",
            icon='FILE_BLEND'
        )
        box.operator(
            "logic_nodes.open_upbge_manual",
            text="Manual",
            icon='BLENDER'
        )
        box = layout.box()
        box.operator(
            "logic_nodes.open_github",
            text="Github Sources",
            icon='MODIFIER_ON'
        )
        box.operator(
            "logic_nodes.open_donate",
            text="Support Logic Nodes",
            icon='FUND'
        )
        box = layout.box()
        col = box.column(align=True)
        col.operator('logic_nodes.install_uplogic', icon='IMPORT', text='Get Uplogic')
        col.prop(preferences(), 'uplogic_version', text='')
