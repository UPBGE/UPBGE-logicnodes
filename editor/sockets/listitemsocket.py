from .socket import SOCKET_TYPE_GENERIC, NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicListItem(NodeSocket, NodeSocketLogic):
    bl_idname = "NLListItemSocket"
    bl_label = "Parameter"
    nl_type = SOCKET_TYPE_GENERIC

    def draw(self, context, layout, node, text):
        row = layout.row(align=True)
        row.label(text=text)
        row.operator('logic_nodes.remove_socket', icon='X', text='')

    def get_unlinked_value(self):
        return None
