import bpy
from .interface import ui_list


@ui_list
class LOGIC_NODES_UL_global_category(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)