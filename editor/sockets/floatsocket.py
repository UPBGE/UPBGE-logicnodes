from .socket import SOCKET_TYPE_BOOL, SOCKET_TYPE_CONDITION, SOCKET_TYPE_FLOAT, SOCKET_TYPE_INT, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicFloat(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFloatFieldSocket"
    bl_label = "Float Value"

    value: FloatProperty(default=0, update=update_draw)

    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_FLOAT
    valid_sockets = [
        SOCKET_TYPE_FLOAT,
        SOCKET_TYPE_INT,
        SOCKET_TYPE_BOOL,
        SOCKET_TYPE_CONDITION
    ]

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
