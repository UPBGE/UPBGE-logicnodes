from .socket import NodeSocketLogic
from .socket import PARAM_VECTOR_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVector(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVectorSocket"
    bl_label = "Parameter"
    type: StringProperty(default='VECTOR')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
