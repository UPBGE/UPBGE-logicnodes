from .socket import SOCKET_TYPE_CONDITION, NodeSocketLogic
from .socket import SOCKET_COLOR_BOOLEAN
from .socket import SOCKET_TYPE_BOOL
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicBoolean(NodeSocket, NodeSocketLogic):
    bl_idname = "NLBooleanSocket"
    bl_label = "Boolean"

    default_value: BoolProperty(name='Boolean', update=update_draw)
    # XXX: Remove value property
    value: BoolProperty(name='Boolean', update=update_draw)
    use_toggle: BoolProperty(default=False)

    nl_type = SOCKET_TYPE_BOOL
    valid_sockets = [SOCKET_TYPE_BOOL, SOCKET_TYPE_CONDITION]
    nl_color = SOCKET_COLOR_BOOLEAN

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=self.name, toggle=self.use_toggle)

    def get_unlinked_value(self):
        return self.default_value
