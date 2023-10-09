from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_add_socket(Operator):
    bl_idname = "logic_nodes.add_socket"
    bl_label = "Add Socket"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a socket to this node"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        node = context.node
        node.inputs.new('NLListItemSocket', self.name)
        node.set_new_input_name()
        return {"FINISHED"}