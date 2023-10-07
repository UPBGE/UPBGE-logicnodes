
from .socket import NodeSocketLogic
from .socket import PARAM_PYTHON_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicPython(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPythonSocket"
    bl_label = "Python"

    color = PARAM_PYTHON_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"

