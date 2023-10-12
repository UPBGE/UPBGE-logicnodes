from .socket import SOCKET_TYPE_GENERIC, NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.types import NodeLink


@socket_type
class NodeSocketLogicParameter(NodeSocket, NodeSocketLogic):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"
    nl_type = SOCKET_TYPE_GENERIC

    # def validate(self, link: NodeLink, from_socket: NodeSocketLogic):
    #     self.nl_color = from_socket.nl_color
    #     link.is_valid = True

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
