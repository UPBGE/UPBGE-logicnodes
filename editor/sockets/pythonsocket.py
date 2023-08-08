
from .socket import NodeSocketLogic
from .socket import PARAM_PYTHON_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicPython(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPythonSocket"
    bl_label = "Python"

    def draw_color(self, context, node):
        return PARAM_PYTHON_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"

