import typing
from .operator import operator
from bpy.types import Context, Operator
from ..generator.tree_code_generator import generate_logic_node_code
import bpy


@operator
class LOGIC_NODES_OT_add_logic_tree_property(Operator):
    bl_idname = "logic_nodes.add_logic_tree_property"
    bl_label = "Add Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Adds a property available to the UPBGE"

    @classmethod
    def poll(cls, context):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        return tree is not None and context.active_object is not None

    def execute(self, context: Context):
        tree = getattr(bpy.context.space_data, 'edit_tree')
        prop = tree.properties.add()
        prop.name = prop.name
        generate_logic_node_code()
        bpy.ops.logic_nodes.reload_components()
        return {'FINISHED'}

    # def invoke(self, context, event):
    #     return {'RUNNING_MODAL'}

    # def modal(self, context, event):
    #     return {'FINISHED'}
