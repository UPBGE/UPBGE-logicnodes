
from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_CONDITION
from .socket import socket_type
from .socket import update_draw
from .socket import SOCKET_TYPE_BOOL
from .socket import SOCKET_TYPE_CONDITION
from bpy.types import NodeSocket
from bpy.props import BoolProperty


@socket_type
class NodeSocketLogicBoolCondition(NodeSocket, NodeSocketLogic):
    """[DEPRECATED]"""
    bl_idname = "NLPseudoConditionSocket"
    bl_label = "Condition"
    nl_color = SOCKET_COLOR_CONDITION
    nl_type = SOCKET_TYPE_CONDITION
    valid_sockets = [SOCKET_TYPE_BOOL, SOCKET_TYPE_CONDITION]

    default_value: BoolProperty(name='Condition', update=update_draw)
    # XXX: Remove value property
    value: BoolProperty(name='Condition', update=update_draw)


    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            layout.prop(self, "default_value", text=label)

    def get_unlinked_value(self):
        return self.default_value
