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
        layout.operator('logic_nodes.custom_node_templates', text='Load Custom Node Templates')
        layout.operator('logic_nodes.register_custom_node', text='Register Custom Node')
        layout.separator()
        layout.label(text='Loaded Nodes:')
        for i, cn in enumerate(preferences().custom_logic_nodes):
            box = layout.box()
            row = box.row()
            row.label(text=cn.label)
            buttons = row.row(align=True)
            edibut = buttons.operator('logic_nodes.edit_custom_node', text='', icon='GREASEPENCIL')
            edibut.index = i
            savbut = buttons.operator('logic_nodes.save_custom_node', text='', icon='FILE_REFRESH')
            savbut.index = i
            rembut = buttons.operator('logic_nodes.remove_custom_node', text='', icon='X')
            rembut.index = i