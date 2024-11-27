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
    bl_label = "Global Property"

    default_value: StringProperty(
        update=update_draw
    )
    # XXX: Remove value property
    value: StringProperty(
        update=update_draw
    )
    ref_index: IntProperty(
        update=update_draw
    )

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            ref_socket = self.node.inputs[self.ref_index]
            if ref_socket.linked_valid:
                col.prop(self, 'default_value', text='')
            else:
                cat = context.scene.nl_global_categories.get(ref_socket.default_value)
                if cat:
                    col.prop_search(
                        self,
                        "default_value",
                        cat,
                        'content',
                        icon='DOT',
                        text=''
                    )
                else:
                    layout.label(text=text)

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)
