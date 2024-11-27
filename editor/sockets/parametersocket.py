from .socket import SOCKET_COLOR_GENERIC, SOCKET_TYPE_GENERIC, NodeSocketLogic
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicParameter(NodeSocket, NodeSocketLogic):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"
    nl_type = SOCKET_TYPE_GENERIC
    nl_color = SOCKET_COLOR_GENERIC

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
