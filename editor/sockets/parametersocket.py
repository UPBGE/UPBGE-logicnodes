from .socket import PARAMETER_SOCKET_COLOR
from .socket import NodeSocketLogic
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicParameter(NodeSocket, NodeSocketLogic):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"
    nl_color = PARAMETER_SOCKET_COLOR

    def draw_color(self, context, node):
        return self.nl_color

    def validate(self, from_socket):
        self.nl_color = from_socket.nl_color

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
