import bpy
from .interface import ui_list


@ui_list
class LOGIC_NODES_UL_global_value(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        dat = {
            'STRING': 'string_val',
            'FLOAT': 'float_val',
            'INTEGER': 'int_val',
            'BOOLEAN': 'bool_val',
            'FILE_PATH': 'filepath_val'
        }
        row = layout.split()
        row.prop(item, "name", text="", emboss=False)
        emboss = item.value_type == 'BOOLEAN' or item.value_type == 'STRING'
        row.prop(item, dat.get(item.value_type, 'FLOAT'), text='', emboss=emboss)
