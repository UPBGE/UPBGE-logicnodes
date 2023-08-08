from .socket import NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicDictionary(NodeSocket, NodeSocketLogic):
    bl_idname = "NLDictSocket"
    bl_label = "Parameter"
    type: StringProperty(default='INT')

    def draw_color(self, context, node):
        return PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"