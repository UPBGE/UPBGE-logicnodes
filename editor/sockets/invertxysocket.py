from .socket import SOCKET_TYPE_DICTIONARY, NodeSocketLogic
from .socket import SOCKET_COLOR_DICTIONARY
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import BoolVectorProperty


@socket_type
class NodeSocketLogicInvertXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Invert XY"
    default_value: BoolVectorProperty(name='XY', size=2)

    nl_color = SOCKET_COLOR_DICTIONARY
    nl_type = SOCKET_TYPE_DICTIONARY

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row(align=True)
            row.label(text='Invert XY:')
            row.prop(self, 'default_value', text='')

    def get_unlinked_value(self):
        return f"dict(x={self.default_value[0]}, y={self.default_value[1]})"
