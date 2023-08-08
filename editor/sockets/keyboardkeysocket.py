from .socket import NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
from .socket import socket_type
from ..enum_types import _enum_field_value_types
from ...utilities import key_event
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicKeyboardKey(NodeSocket, NodeSocketLogic):
    bl_idname = "NLKeyboardKeySocket"
    bl_label = "Key"
    value: StringProperty(update=update_draw)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def get_unlinked_value(self):
        return key_event(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = self.value
            if not label:
                label = "Press & Choose"
            layout.operator("logic_nodes.wait_for_key", text=label)
