import bpy

from ..utilities import make_valid_name
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree


@ui_panel
class LOGIC_NODES_PT_logic_tree_properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"

    @classmethod
    def poll(cls, context):
        if not getattr(context.space_data, 'edit_tree', None):
            return False
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.edit_tree
        layout.operator("logic_nodes.add_logic_tree_property", text='Add', icon='PLUS')
        for i, prop in enumerate(tree.properties):
            box = layout.box()
            row = box.row(align=True)
            row.prop(prop, 'name', text='')
            row.prop(prop, 'value_type', text='')
            rem = row.operator("logic_nodes.remove_logic_tree_property", text='', icon='X')
            rem.prop_index = i
            obj = bpy.context.view_layer.objects.active
            if obj:
                row = box.row(align=True)
                comp = obj.game.components.get(make_valid_name(tree.name))
                if not comp:
                    continue
                cprop = comp.properties[prop.name]
                row.prop(cprop, 'value', text='')
                vtype = int(prop.value_type)
                # if vtype = 13:
                #     row.operator('logic_nodes.load_text')
                if vtype == 14:
                    row.operator('logic_nodes.load_sound', text='', icon='FILEBROWSER')
                elif vtype == 15:
                    row.operator('logic_nodes.load_image', text='', icon='FILEBROWSER')
                elif vtype == 16:
                    row.operator('logic_nodes.load_font', text='', icon='FILEBROWSER')