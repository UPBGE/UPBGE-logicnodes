from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicGlobalProperty(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGlobalPropSocket"
    bl_label = "Category"

    value: StringProperty(
        update=update_draw
    )
    ref_index: IntProperty(
        update=update_draw
    )

    color = SOCKET_COLOR_STRING
    nl_color = SOCKET_TYPE_STRING

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            ref_socket = self.node.inputs[self.ref_index]
            if ref_socket.is_linked:
                col.prop(self, 'value', text='')
            else:
                cat = context.scene.nl_global_categories.get(ref_socket.value)
                if cat:
                    col.prop_search(
                        self,
                        "value",
                        cat,
                        'content',
                        icon='DOT',
                        text=''
                    )
                else:
                    layout.label(text=text)

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)
