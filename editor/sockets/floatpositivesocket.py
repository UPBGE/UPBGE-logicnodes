from .socket import SOCKET_TYPE_BOOL, SOCKET_TYPE_CONDITION, SOCKET_TYPE_FLOAT, SOCKET_TYPE_INT, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
import bpy


@socket_type
class NodeSocketLogicFloatPositive(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPositiveFloatSocket"
    bl_label = "Positive Float"

    default_value: FloatProperty(min=0.0, update=update_draw)
    # XXX: Remove value property
    value: FloatProperty(min=0.0, update=update_draw)

    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_FLOAT
    valid_sockets = [
        SOCKET_TYPE_FLOAT,
        SOCKET_TYPE_INT,
        SOCKET_TYPE_BOOL,
        SOCKET_TYPE_CONDITION
    ]

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.default_value)
