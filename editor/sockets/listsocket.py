from .socket import SOCKET_TYPE_LIST, NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicList(NodeSocket, NodeSocketLogic):
    bl_idname = "NLListSocket"
    bl_label = "List"
    nl_shape = 'SQUARE'
    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_LIST

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return None
