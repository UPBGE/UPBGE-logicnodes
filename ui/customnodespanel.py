import bpy
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree
from ..utilities import preferences


@ui_panel
class LOGIC_NODES_PT_custom_nodes(bpy.types.Panel):
    bl_label = "Custom Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Custom Nodes"

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        for cn in preferences().custom_logic_nodes:
            row = layout.row()
            row.label(text=cn.label)
            row.operator('logic_nodes.remove_custom_node', text='', icon='X')