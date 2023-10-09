from .operator import operator
from bpy.types import Operator



@operator
class LOGIC_NODES_OT_remove_socket(Operator):
    bl_idname = "logic_nodes.remove_socket"
    bl_label = "Remove"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove this socket"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        socket = context.socket
        node = context.node
        node.inputs.remove(socket)
        return {"FINISHED"}