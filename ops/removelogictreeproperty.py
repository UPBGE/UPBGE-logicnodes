from .operator import operator
from bpy.types import Operator
from ..editor.nodetree import LogicNodeTree
from bpy.props import IntProperty
import bpy


@operator
class LOGIC_NODES_OT_remove_logic_tree_property(Operator):
    bl_idname = "logic_nodes.remove_logic_tree_property"
    bl_label = "Remove Logic Tree Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove a value accessible from anywhere"

    prop_index: IntProperty()

    @classmethod
    def poll(cls, context):
        if not getattr(context.space_data, 'edit_tree', None):
            return False
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def execute(self, context):
        tree = context.space_data.edit_tree
        props = tree.properties
        props.remove(self.prop_index)
        tree.changes_staged = True
        bpy.ops.logic_nodes.generate_code()
        bpy.ops.logic_nodes.reload_components()
        return {'FINISHED'}