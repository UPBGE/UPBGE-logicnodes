from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
import bpy


@socket_type
class NodeSocketLogicGlobalCategory(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGlobalCatSocket"
    bl_label = "Global Category"

    default_value: StringProperty(
        update=update_draw
    )
    # XXX: Remove value property
    value: StringProperty(
        update=update_draw
    )

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            col.prop_search(
                self,
                "default_value",
                context.scene,
                'nl_global_categories',
                icon='OUTLINER_COLLECTION',
                text=''
            )

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)
