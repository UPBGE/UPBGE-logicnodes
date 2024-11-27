from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import SOCKET_TYPE_INT
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_local_oriented_axis
from bpy.types import NodeSocket
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicAxisSigned(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketOrientedLocalAxis"
    bl_label = "Signed Axis"

    default_value: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis,
        update=update_draw
    )

    # XXX: Remove value property
    value: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis,
        update=update_draw
    )

    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def _draw(self, context, layout, node, text):
        if self.linked_valid:
            layout.label(text=text)
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "default_value", text='')

    def get_unlinked_value(self):
        return self.default_value
