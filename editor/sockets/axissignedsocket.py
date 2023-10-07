from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_local_oriented_axis
from bpy.types import NodeSocket
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicAxisSigned(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketOrientedLocalAxis"
    bl_label = "Local Axis"

    value: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis,
        update=update_draw
    )

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "value", text='')

    def get_unlinked_value(self):
        return self.value
