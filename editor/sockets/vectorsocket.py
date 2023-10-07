from .socket import NodeSocketLogic
from .socket import PARAM_VECTOR_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVector(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVectorSocket"
    bl_label = "Parameter"
    type: StringProperty(default='VECTOR')

    color = PARAM_VECTOR_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
