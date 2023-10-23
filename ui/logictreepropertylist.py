import bpy
from .interface import ui_list


@ui_list
class LOGIC_NODES_UL_logic_tree_property(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        row = layout.split()
        row.prop(item, "name", text="", emboss=False)
        emboss = item.value_type == 'BOOLEAN' or item.value_type == 'STRING'
        row.prop(item, getattr(item.value_type, 'FLOAT'), text='', emboss=emboss)
