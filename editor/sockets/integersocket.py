from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import SOCKET_TYPE_INT
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import IntProperty


@socket_type
class NodeSocketLogicInteger(NodeSocket, NodeSocketLogic):
    bl_idname = "NLIntegerFieldSocket"
    bl_label = "Integer"
    nl_type = SOCKET_TYPE_INT
    nl_color = SOCKET_COLOR_INTEGER

    default_value: IntProperty(update=update_draw)
    # XXX: Remove value property
    value: IntProperty(update=update_draw)

    def get_unlinked_value(self):
        return '{}'.format(self.default_value)

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)
