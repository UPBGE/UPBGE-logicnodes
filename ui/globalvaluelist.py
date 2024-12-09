import bpy
from .interface import ui_list


@ui_list
class LOGIC_NODES_UL_global_value(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        dat = {
            '0': 'float_val',
            '1': 'string_val',
            '2': 'int_val',
            '3': 'bool_val',
            '17': 'filepath_val',
            '4': 'vec_val',
            '5': 'color_val',
            '6': 'color_alpha_val',
            '7': 'obj_val',
            '8': 'collection_val',
            '9': 'material_val',
            '10': 'mesh_val',
            '11': 'node_tree_val',
            '12': 'action_val',
            '13': 'text_val',
            '14': 'sound_val',
            '15': 'image_val',
            '16': 'font_val'
        }
        row = layout.split()
        row.prop(item, "name", text="", emboss=False)
        emboss = item.value_type == 'BOOLEAN' or item.value_type == 'STRING'
        row.prop(item, dat.get(item.value_type, 'FLOAT'), text='', emboss=True)
