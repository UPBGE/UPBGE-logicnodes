
from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_CONDITION
from .socket import socket_type
from .socket import SOCKET_TYPE_BOOL
from .socket import SOCKET_TYPE_CONDITION
from bpy.types import NodeSocket
from bpy.props import BoolProperty


@socket_type
class NodeSocketLogicBoolCondition(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPseudoConditionSocket"
    bl_label = "Condition"
    nl_type = SOCKET_TYPE_CONDITION
    valid_sockets = [SOCKET_TYPE_BOOL, SOCKET_TYPE_CONDITION]
    value: BoolProperty(
        name='Condition',
        description=(
            'Optional; When True, '
            'perform with each frame, when False, never perform'
        ))

    nl_color = SOCKET_COLOR_CONDITION

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            layout.prop(self, "value", text=label)

    def get_unlinked_value(self):
        return "True" if self.value else "False"
