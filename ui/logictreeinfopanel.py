import bpy
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree
from ..utilities import make_valid_name


@ui_panel
class LOGIC_NODES_PT_logic_tree_info_panel(bpy.types.Panel):
    bl_label = "Tree applied to:"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        if not getattr(context.space_data, 'edit_tree', None):
            return False
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw_owner(self, obj, container, prop, tree):
        layout = container.box()
        row = layout.split()
        name = row.row()
        name.alignment = 'LEFT'
        name.prop(prop, 'value', text='')
        name.label(text=obj.name)
        row = row.row(align=True)
        row.alignment = 'RIGHT'
        op = row.operator(
            'logic_nodes.get_owner',
            text="",
            icon="RESTRICT_SELECT_OFF"
        )
        op.applied_object = obj.name

        op = row.operator(
            'logic_nodes.unapply_logic_tree',
            text="",
            icon="X"
        )
        op.tree_name = tree.name
        op.from_obj_name = obj.name

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.edit_tree
        container = layout.column(align=True)
        for obj in bpy.data.objects:
            pname = f'NL__{make_valid_name(tree.name)}'
            if pname in obj.game.properties and obj.name in bpy.context.view_layer.objects:
                prop = obj.game.properties[pname]
                self.draw_owner(obj, container, prop, tree)
