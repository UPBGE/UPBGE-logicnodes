
from .socket import SOCKET_TYPE_PYTHON, NodeSocketLogic
from .socket import SOCKET_COLOR_PYTHON
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicPython(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPythonSocket"
    bl_label = "Python"

    nl_color = SOCKET_COLOR_PYTHON
    nl_type = SOCKET_TYPE_PYTHON
    valid_sockets = []

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"

