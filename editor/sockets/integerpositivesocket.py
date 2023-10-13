from .socket import SOCKET_TYPE_INT, NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import IntProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicIntegerPositive(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPositiveIntegerFieldSocket"
    bl_label = "Integer"

    value: IntProperty(min=0, default=0, update=update_draw)
    color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)
