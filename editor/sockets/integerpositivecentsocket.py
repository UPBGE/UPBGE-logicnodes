from .socket import SOCKET_TYPE_INT, NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import IntProperty

@socket_type
class NodeSocketLogicIntegerPositiveCent(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPositiveIntCentSocket"
    bl_label = "Positive Integer Cent"

    default_value: IntProperty(
        min=0,
        max=100,
        default=0,
        update=update_draw
    )
    # XXX: Remove value property
    value: IntProperty(
        min=0,
        max=100,
        default=0,
        update=update_draw
    )
    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.default_value)
