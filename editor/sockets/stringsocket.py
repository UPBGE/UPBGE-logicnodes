from .socket import SOCKET_COLOR_STRING, SOCKET_TYPE_GENERIC
from .socket import SOCKET_TYPE_VALUE
from .socket import SOCKET_TYPE_STRING
from .socket import NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import BoolProperty


class Base(NodeSocket, NodeSocketLogic):

    default_value: StringProperty(update=update_draw)
    # XXX: Remove value property
    value: StringProperty(update=update_draw)
    formatted: BoolProperty(update=update_draw)

    nl_color = SOCKET_COLOR_STRING
    # nl_type = SOCKET_TYPE_STRING
    nl_type = SOCKET_TYPE_GENERIC

    # valid_sockets = [
    #     SOCKET_TYPE_VALUE,
    #     SOCKET_TYPE_STRING
    # ]

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        elif not text:
            layout.prop(self, "default_value", text='')
        else:
            if self.formatted:
                col = layout.column()
                row1 = col.row()
                row1.label(text=text)
                row2 = col.row()
                row2.prop(self, 'default_value', text='')
            else:
                parts = layout.split(factor=.4)
                parts.label(text=text)
                parts.prop(self, "default_value", text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)


@socket_type
class NodeSocketLogicString(Base):
    bl_idname = "NodeSocketLogicString"
    bl_label = "String"


@socket_type
class NLQuotedStringFieldSocket(Base):
    bl_idname = "NLQuotedStringFieldSocket"
    bl_label = "String"
