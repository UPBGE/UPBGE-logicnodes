from .socket import NodeSocketLogic
from .socket import PARAM_IMAGE_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import Image
from bpy.types import NodeSocket
from bpy.props import PointerProperty


@socket_type
class NodeSocketLogicImage(NodeSocket, NodeSocketLogic):
    bl_idname = "NLImageSocket"
    bl_label = "Image"
    value: PointerProperty(
        name='Image',
        type=Image,
        description='Select an Image'
        # update=update_tree_code
    )

    color = PARAM_IMAGE_SOCKET_COLOR

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
                'logic_nodes.load_image',
                icon='FILEBROWSER',
                text=''
            )

    def get_unlinked_value(self):
        if self.value is None:
            return '"None"'
        return f'bpy.data.images.get("{self.value.name}")'
        # return '"{}"'.format(str(self.value.name))
