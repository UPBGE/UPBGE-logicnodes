import typing
from .socket import SOCKET_COLOR_CONDITION, SOCKET_COLOR_GENERIC, SOCKET_COLOR_STRING, SOCKET_TYPE_GENERIC
from .socket import NodeSocketLogic
from .socket import SOCKET_TYPE_CONDITION
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.types import UILayout


@socket_type
class NodeSocketLogicRemovable(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicRemovable"
    bl_label = "List Item"
    nl_type = SOCKET_TYPE_GENERIC
    nl_color = SOCKET_COLOR_GENERIC

    def _draw(self, context, layout, node, text):
        row = layout.row(align=False)
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
    nl_type = SOCKET_TYPE_CONDITION
    nl_color = SOCKET_COLOR_CONDITION


@socket_type
class NodeSocketLogicArgumentItem(NodeSocketLogicRemovable):
    bl_idname = 'NodeSocketLogicArgumentItem'
    bl_label = 'Argument'
    nl_color = SOCKET_COLOR_GENERIC
    argument_name: StringProperty(name='Argument Name', default='Argument')

    def draw(self, context, layout: UILayout, node, text):
        row = layout.row()
        row.prop(self, 'argument_name', text='', emboss=False)
        row.operator('logic_nodes.remove_socket', icon='X', text='')


@socket_type
class NodeSocketLogicStringItem(NodeSocketLogicRemovable):
    bl_idname = 'NodeSocketLogicStringItem'
    bl_label = 'String'
    nl_color = SOCKET_COLOR_STRING

    default_value: StringProperty(name='String', default='')

    def draw(self, context, layout: UILayout, node, text):
        row = layout.row()
        if not self.is_linked:
            row.prop(self, 'default_value', text='')
        else:
            row.label(text=self.name)
        row.operator('logic_nodes.remove_socket', icon='X', text='')

    def get_unlinked_value(self):
        return repr(self.default_value)
