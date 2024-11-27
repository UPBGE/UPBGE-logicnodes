from .socket import SOCKET_TYPE_IMAGE, NodeSocketLogic
from .socket import SOCKET_COLOR_DATABLOCK
from .socket import socket_type
from .socket import update_draw
from bpy.types import Image
from bpy.types import NodeSocket
from bpy.props import PointerProperty


@socket_type
class NodeSocketLogicImage(NodeSocket, NodeSocketLogic):
    bl_idname = "NLImageSocket"
    bl_label = "Image"
    default_value: PointerProperty(
        name='Image',
        type=Image,
        description='Select an Image'
        # update=update_tree_code
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Image',
        type=Image,
        description='Select an Image'
        # update=update_tree_code
    )

    nl_color = SOCKET_COLOR_DATABLOCK
    nl_type = SOCKET_TYPE_IMAGE

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                row = col.row(align=True)
                row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "default_value", text='')
            row2.operator(
                'logic_nodes.load_image',
                icon='FILEBROWSER',
                text=''
            )

    def get_unlinked_value(self):
        if self.default_value is None:
            return '"None"'
        return f'bpy.data.images.get("{self.default_value.name}")'
