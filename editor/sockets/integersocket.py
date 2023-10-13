from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import SOCKET_TYPE_INT
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import IntProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicInteger(NodeSocket, NodeSocketLogic):
    bl_idname = "NLIntegerFieldSocket"
    bl_label = "Integer"
    nl_type = SOCKET_TYPE_INT
    color = SOCKET_COLOR_INTEGER

    value: IntProperty(update=update_draw)

    def get_unlinked_value(self):
        return '{}'.format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)