from .socket import SOCKET_COLOR_INTEGER, SOCKET_TYPE_INT, NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_local_axis
from bpy.types import NodeSocket
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicAxis(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketLocalAxis"
    bl_label = "Unsigned Axis"

    default_value: EnumProperty(
        name='Axis',
        items=_enum_local_axis,
        update=update_draw
    )
    # XXX: Remove value property
    value: EnumProperty(
        name='Axis',
        items=_enum_local_axis,
        update=update_draw
    )

    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def __init__(self):
        NodeSocketLogic.__init__(self)

    def _draw(self, context, layout, node, text):
        if self.linked_valid:
            layout.label(text=text)
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "default_value", text='')

    def get_unlinked_value(self):
        return self.default_value
