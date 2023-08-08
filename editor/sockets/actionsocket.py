from .socket import NodeSocketLogic
from .socket import ACTION_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicAction(NodeSocket, NodeSocketLogic):
    bl_idname = "NLActionSocket"
    bl_label = "Action"

    def draw_color(self, context, node):
        return ACTION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)
