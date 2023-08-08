from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
import bpy


@socket_type
class NodeSocketLogicFloatPositive(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPositiveFloatSocket"
    bl_label = "Positive Float"
    value: FloatProperty(min=0.0, update=update_draw)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)
