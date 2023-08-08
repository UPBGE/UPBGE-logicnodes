from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
import bpy


@socket_type
class NodeSocketLogicGlobalCategory(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGlobalCatSocket"
    bl_label = "Category"
    value: StringProperty(
        update=update_draw
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            col.prop_search(
                self,
                "value",
                context.scene,
                'nl_global_categories',
                icon='OUTLINER_COLLECTION',
                text=''
            )

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)
