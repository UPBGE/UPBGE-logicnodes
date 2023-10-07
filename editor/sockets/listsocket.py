from .socket import NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicList(NodeSocket, NodeSocketLogic):
    bl_idname = "NLListSocket"
    bl_label = "Parameter"
    type: StringProperty(default='RGBA')
    color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"
