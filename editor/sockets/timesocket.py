from .socket import SOCKET_TYPE_FLOAT, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicTime(NodeSocket, NodeSocketLogic):
    bl_idname = "NLTimeSocket"
    bl_label = "Time"

    default_value: FloatProperty(
        min=0,
        default=0,
        subtype='TIME',
        unit='TIME',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_FLOAT

    def get_unlinked_value(self):
        return "{}".format(self.default_value)

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)
