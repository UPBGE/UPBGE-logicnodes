from .socket import SOCKET_TYPE_DICTIONARY, NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicDictionary(NodeSocket, NodeSocketLogic):
    bl_idname = "NLDictSocket"
    bl_label = "Parameter"

    color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_DICTIONARY

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"