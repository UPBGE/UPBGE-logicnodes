from .socket import SOCKET_TYPE_DICTIONARY, SOCKET_TYPE_LIST, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicInvertXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Invert XY"

    x: BoolProperty(update=update_draw)
    y: BoolProperty(update=update_draw)

    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_DICTIONARY

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
