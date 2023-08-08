from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicFloat(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFloatFieldSocket"
    bl_label = "Float Value"
    value: FloatProperty(default=0, update=update_draw)
    valid_sockets = ['NLFloatFieldSocket']

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
