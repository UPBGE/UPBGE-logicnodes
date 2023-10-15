from .socket import SOCKET_COLOR_CONDITION, SOCKET_COLOR_GENERIC, SOCKET_TYPE_GENERIC, NodeSocketLogic
from .socket import socket_type
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicRemovable(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicRemovable"
    bl_label = "List Item"
    nl_type = SOCKET_TYPE_GENERIC
    nl_color = SOCKET_COLOR_GENERIC

    def draw(self, context, layout, node, text):
        row = layout.row(align=True)
        row.label(text=text)
        row.operator('logic_nodes.remove_socket', icon='X', text='')

    def get_unlinked_value(self):
        return None


@socket_type
class NodeSocketLogicListItem(NodeSocketLogicRemovable):
    bl_idname = 'NLListItemSocket'
    bl_label = 'Item'
    nl_color = SOCKET_COLOR_GENERIC


@socket_type
class NodeSocketLogicConditionItem(NodeSocketLogicRemovable):
    bl_idname = 'NodeSocketLogicConditionItem'
    bl_label = 'Condition'
    nl_color = SOCKET_COLOR_CONDITION
