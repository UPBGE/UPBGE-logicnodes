import bpy
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree


@ui_panel
class LOGIC_NODES_PT_templates(bpy.types.Panel):
    bl_label = "Manage"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        pack_new = layout.column()
        pack_new.scale_y = 1.4
        pack_new.operator(
            'logic_nodes.pack_new_tree',
            icon='IMPORT'
        )

        layout.separator()
        prefabs = layout.box()
        title = prefabs.box()
        title.label(text='Node Templates:')
        template_col = prefabs.column()
        template_col.scale_y = 1.4
        op = template_col.operator(
            'logic_nodes.add_template',
            icon='LAYER_ACTIVE',
            text='4-Key Template'
        )
        op.nl_template_name = '4keymovement'