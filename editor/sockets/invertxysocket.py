from ...utilities import DEPRECATED
from .socket import SOCKET_TYPE_DICTIONARY, NodeSocketLogic
from .socket import SOCKET_COLOR_DICTIONARY
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import BoolVectorProperty
from bpy.props import BoolProperty


@socket_type
class NodeSocketLogicInvertXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Invert XY"
    nl_color = SOCKET_COLOR_DICTIONARY
    nl_type = SOCKET_TYPE_DICTIONARY

    default_value: BoolVectorProperty(name='XY', size=2)
    # XXX: Remove value property
    value: BoolVectorProperty(name='XY', size=2)

    x: BoolProperty()
    y: BoolProperty()

    def _update_prop_name(self):
        # XXX: Remove value override
        x = getattr(self, 'x', DEPRECATED)
        y = getattr(self, 'y', DEPRECATED)
        if x is not DEPRECATED:
            self.default_value[0] = x
        if y is not DEPRECATED:
            self.default_value[1] = y

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            row = layout.row(align=True)
            row.label(text='Invert XY:')
            row.prop(self, 'default_value', text='')

    def get_unlinked_value(self):
        return f"[{self.default_value[0]}, {self.default_value[1]}]"
