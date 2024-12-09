import bpy

from ..utilities import make_valid_name
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree
from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty


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
            row.prop(prop, 'show_prop', text='', icon='HIDE_OFF' if prop.show_prop else 'HIDE_ON')
            rem = row.operator("logic_nodes.remove_logic_tree_property", text='', icon='X')
            rem.prop_index = i
            obj = bpy.context.view_layer.objects.active
            if obj:
                comp = obj.game.components.get(make_valid_name(tree.name))
                if not prop.show_prop:
                    continue
                col = box.column()
                row = col.row(align=True)
                if not comp:
                    box.label(text='Tree must be applied to Object!', icon='ERROR')
                    continue
                cprop = comp.properties[prop.name]
                vtype = int(prop.value_type)
                if vtype in [5, 6]:
                    row.template_color_picker(cprop, 'value', value_slider=True, lock=True, lock_luminosity=True, cubic=True)
                elif vtype == 4:
                    col.prop(cprop, 'value', text='')
                else:
                    row.prop(cprop, 'value', text='')
                # if vtype = 13:
                #     row.operator('logic_nodes.load_text')
                if vtype == 14:
                    row.operator('logic_nodes.load_sound', text='', icon='FILEBROWSER')
                elif vtype == 15:
                    row.operator('logic_nodes.load_image', text='', icon='FILEBROWSER')
                elif vtype == 16:
                    row.operator('logic_nodes.load_font', text='', icon='FILEBROWSER')
