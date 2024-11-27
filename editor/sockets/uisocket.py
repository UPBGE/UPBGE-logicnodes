from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_MESH
from .socket import SOCKET_TYPE_UI
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicUI(NodeSocket, NodeSocketLogic):
    bl_idname = "NLUISocket"
    bl_label = "UI Element"
    nl_color = SOCKET_COLOR_MESH
    nl_type = SOCKET_TYPE_UI

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"