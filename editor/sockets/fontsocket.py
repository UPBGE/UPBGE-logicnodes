from .socket import SOCKET_TYPE_FONT, NodeSocketLogic
from .socket import SOCKET_COLOR_IMAGE
from .socket import socket_type
from .socket import update_draw
from bpy.types import VectorFont
from bpy.types import NodeSocket
from bpy.props import PointerProperty


@socket_type
class NodeSocketLogicFont(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFontSocket"
    bl_label = "Font"
    default_value: PointerProperty(
        name='Font',
        type=VectorFont,
        description='Select a Font',
        update=update_draw
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Font',
        type=VectorFont,
        description='Select a Font',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_IMAGE
    nl_type = SOCKET_TYPE_FONT

    def draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                row = col.row(align=True)
                row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "default_value", text='')
            row2.operator(
                'logic_nodes.load_font', icon='FILEBROWSER', text='')

    def get_unlinked_value(self):
        if self.default_value is None:
            return '""'
        return f'bpy.data.fonts.get("{self.default_value.name}")'
