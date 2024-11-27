from ..utilities import error
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
from ..editor.nodetree import LogicNodeTree
from ..editor.nodes.node import _nodes
import bpy


error('DEBUG OPERATOR LOADED: LOGIC_NODES_OT_add_all_nodes')


@operator
class LOGIC_NODES_OT_add_all_nodes(Operator):
    bl_idname = "logic_nodes.add_all_nodes"
    bl_label = "Add All Nodes"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add all logic nodes at once (DEBUG)"

    @classmethod
    def poll(cls, context):
        tree = getattr(context.space_data, 'edit_tree')
        if tree is None:
            return False
        return isinstance(tree, LogicNodeTree)

    def execute(self, context):
        pos_x = 0
        for node in _nodes:
            print(f'Adding {node.bl_idname}...')
            if not node.deprecated:
                bpy.ops.node.add_node(type=node.bl_idname)
                node = context.space_data.edit_tree.nodes[-1]
                node.location = (pos_x, 0)
                pos_x += 200
                node.check_socket_identifiers()
        return {'FINISHED'}