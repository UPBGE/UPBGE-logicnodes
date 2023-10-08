from .socket import NodeSocketLogic
from .socket import PARAM_MESH_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.props import StringProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicUI(NodeSocket, NodeSocketLogic):
    bl_idname = "NLUISocket"
    bl_label = "Parameter"
    color = PARAM_MESH_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"