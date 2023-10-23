from ..props.property import get_global_category
from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_add_global_property(Operator):
    bl_idname = "logic_nodes.add_global_property"
    bl_label = "Add Global Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a value accessible from anywhere"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        category = get_global_category()
        prop = category.content.add()
        prop.name = 'prop'
        prop.string_val = ''
        prop.float_val = 0.0
        prop.int_val = 0
        prop.bool_val = False
        prop.filepath_val = ''
        category.selected = len(category.content) - 1

        return {'FINISHED'}