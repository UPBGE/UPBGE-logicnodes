from .socket import NodeSocketLogic
from .socket import ACTION_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicAction(NodeSocket, NodeSocketLogic):
    bl_idname = "NLActionSocket"
    bl_label = "Action"
    color = ACTION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)
