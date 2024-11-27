from .socket import SOCKET_TYPE_LIST, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicList(NodeSocket, NodeSocketLogic):
    bl_idname = "NLListSocket"
    bl_label = "List"
    nl_shape = 'SQUARE'
    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_LIST
    
    valid_sockets = [SOCKET_TYPE_LIST, SOCKET_TYPE_VECTOR]

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return []
