from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicFilePath(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFilePathSocket"
    bl_label = "Filepath"

    default_value: StringProperty(
        subtype='FILE_PATH',
        update=update_draw
    )
    # XXX: Remove value property
    value: StringProperty(
        subtype='FILE_PATH',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                col.label(text=text)
            col.prop(self, "default_value", text='')

    def get_unlinked_value(self):
        return repr(self.default_value)
