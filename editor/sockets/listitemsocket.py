from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicListItem(NodeSocket, NodeSocketLogic):
    bl_idname = "NLListItemSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        row = layout.row(align=True)
        row.label(text=text)
        row.operator('logic_nodes.remove_list_item_socket', icon='X', text='')

    def get_unlinked_value(self):
        return None
