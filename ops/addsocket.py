from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty


@operator
class LOGIC_NODES_OT_add_socket(Operator):
    bl_idname = "logic_nodes.add_socket"
    bl_label = "Add Socket"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a socket to this node"
    socket_type: StringProperty(default='NLListItemSocket')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        node = context.node
        node.inputs.new(self.socket_type, self.name)
        node.set_new_input_name()
        return {"FINISHED"}