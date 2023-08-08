
from .socket import NodeSocketLogic
from .socket import CONDITION_SOCKET_COLOR
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import BoolProperty


@socket_type
class NodeSocketLogicPseudoCondition(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPseudoConditionSocket"
    bl_label = "Condition"
    value: BoolProperty(
        name='Condition',
        description=(
            'Optional; When True, '
            'perform with each frame, when False, never perform'
        ))

    def draw_color(self, context, node):
        return CONDITION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            layout.prop(self, "value", text=label)

    def get_unlinked_value(self):
        return "True" if self.value else "False"
