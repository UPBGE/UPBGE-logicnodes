from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicInvertXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Boolean"
    x: BoolProperty(update=update_draw)
    y: BoolProperty(update=update_draw)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text='Inverted:')
            row.prop(self, 'x', text="X")
            row.prop(self, 'y', text="Y")

    def get_unlinked_value(self):
        return "dict(x={}, y={})".format(self.x, self.y)
