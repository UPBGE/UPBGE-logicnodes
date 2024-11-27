from .socket import SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_VECTOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVector(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVectorSocket"
    bl_label = "Vector"
    nl_type = SOCKET_TYPE_VECTOR
    nl_color = SOCKET_COLOR_VECTOR
    valid_sockets = [SOCKET_TYPE_VECTOR, SOCKET_TYPE_COLOR]

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
