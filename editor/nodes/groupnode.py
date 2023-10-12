from ..nodetree import LogicNodeTree
from ..sockets import NodeSocketLogicVirtual
from .node import LogicNode
from .node import node_type
from bpy.props import StringProperty
from bpy.types import NodeGroupInput, NodeTree
import bpy


# @node_type
class NodeGroupInputLogic(NodeGroupInput, LogicNode):
    bl_idname = "NodeGroupInputLogic"
    bl_label = 'Group Input'
    nl_module = 'Groupy'
    group_name = StringProperty()
    output_map = {}

    def poll_instance(self, node_tree: NodeTree) -> bool:
        return True

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)
    
    def draw_buttons(self, context, layout):
        pass

    def group_update(self, nodetree):
        self.outputs.clear()
        for i, input in enumerate(nodetree.inputs):
            otp = self.outputs.new(input.bl_socket_idname, input.name)
            self.output_map[input] = otp
        self.add_output(NodeSocketLogicVirtual, '')

    def init(self, context):
        self.output_map = {}
        for i, input in enumerate(bpy.context.space_data.edit_tree.inputs):
            otp = self.outputs.new(input.bl_socket_idname, input.name)
            self.output_map[input] = otp
        self.add_output(NodeSocketLogicVirtual, '')
