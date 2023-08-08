from .socket import NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import IntProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicIntegerPositive(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPositiveIntegerFieldSocket"
    bl_label = "Integer"
    value: IntProperty(min=0, default=0, update=update_draw)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)
