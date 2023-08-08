from .socket import NodeSocketLogic
from .socket import PARAM_IMAGE_SOCKET_COLOR
from .socket import socket_type
from bpy.types import VectorFont
from bpy.types import NodeSocket
from bpy.props import PointerProperty


@socket_type
class NodeSocketLogicFont(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFontSocket"
    bl_label = "Font"
    value: PointerProperty(
        name='Font',
        type=VectorFont,
        description='Select a Font'
        # update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_IMAGE_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                row = col.row(align=True)
                row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "value", text='')
            row2.operator(
                'logic_nodes.load_font', icon='FILEBROWSER', text='')

    def get_unlinked_value(self):
        if self.value is None:
            return '""'
        return '"{}"'.format(str(self.value.name))
