from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import BoolProperty


class Base(NodeSocket, NodeSocketLogic):

    value: StringProperty(update=update_draw)
    formatted: BoolProperty(update=update_draw)

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        elif not text:
            layout.prop(self, "value", text='')
        else:
            if self.formatted:
                col = layout.column()
                row1 = col.row()
                row1.label(text=text)
                row2 = col.row()
                row2.prop(self, 'value', text='')
            else:
                parts = layout.split(factor=.4)
                parts.label(text=text)
                parts.prop(self, "value", text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


@socket_type
class NodeSocketLogicString(Base):
    bl_idname = "NodeSocketLogicString"
    bl_label = "String"


@socket_type
class NLQuotedStringFieldSocket(Base):
    bl_idname = "NLQuotedStringFieldSocket"
    bl_label = "String"
