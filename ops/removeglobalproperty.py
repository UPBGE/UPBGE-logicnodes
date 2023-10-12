from ..props.property import get_global_category
from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_remove_global_property(Operator):
    bl_idname = "logic_nodes.remove_global_property"
    bl_label = "Remove Global Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove a value accessible from anywhere"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        category = get_global_category()
        category.content.remove(category.selected)
        if category.selected > len(category.content) - 1:
            category.selected = len(category.content) - 1
        return {'FINISHED'}