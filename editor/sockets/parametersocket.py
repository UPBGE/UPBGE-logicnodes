from .socket import NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.types import NodeLink


@socket_type
class NodeSocketLogicParameter(NodeSocket, NodeSocketLogic):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"

    def validate(self, link: NodeLink, from_socket: NodeSocketLogic):
        self.nl_color = from_socket.nl_color
        link.is_valid = True

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
