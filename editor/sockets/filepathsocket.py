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

    value: StringProperty(
        subtype='FILE_PATH',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                col.label(text=text)
            col.prop(self, "value", text='')

    def get_unlinked_value(self):
        path = str(self.value)
        path = path.replace('\\', '/')
        if path.endswith('\\'):
            path = path[:-1]
        return '"{}"'.format(path)
