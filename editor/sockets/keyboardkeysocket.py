from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import SOCKET_TYPE_INT
from .socket import socket_type
from .socket import update_draw
from ...utilities import key_event
from bpy.types import NodeSocket
from bpy.props import StringProperty



@socket_type
class NodeSocketLogicKeyboardKey(NodeSocket, NodeSocketLogic):
    bl_idname = "NLKeyboardKeySocket"
    bl_label = "Key"

    default_value: StringProperty(update=update_draw)
    # XXX: Remove value property
    value: StringProperty(update=update_draw)
    nl_color = SOCKET_COLOR_INTEGER

    nl_type = SOCKET_TYPE_INT
    valid_sockets = [SOCKET_TYPE_INT]

    def get_unlinked_value(self):
        return key_event(self.default_value)

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            label = self.default_value
            if not label:
                label = "Press & Choose"
            layout.box().operator("logic_nodes.key_selector", text=label, emboss=False, icon='MOUSE_LMB')
