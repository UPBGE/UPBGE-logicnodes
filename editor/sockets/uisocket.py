from .socket import NodeSocketLogic
from .socket import PARAM_MESH_SOCKET_COLOR
from .socket import socket_type
from bpy.props import StringProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicUI(NodeSocket, NodeSocketLogic):
    bl_idname = "NLUISocket"
    bl_label = "Parameter"
    type: StringProperty(default='GEOMETRY')
    nl_color = PARAM_MESH_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"