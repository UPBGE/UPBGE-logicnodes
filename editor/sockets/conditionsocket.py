from .socket import NodeSocketLogic
from .socket import CONDITION_SOCKET_COLOR
from .socket import socket_type
from bpy.props import StringProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicCondition(NodeSocket, NodeSocketLogic):
    bl_idname = "NLConditionSocket"
    bl_label = "Condition"
    description = StringProperty(default='Execution Condition')
    default_value: StringProperty(
        name='Condition',
        default="None"
    )
    type: StringProperty(default='MATERIAL')
    nl_color = CONDITION_SOCKET_COLOR

    def shape_setup(self):
        self.display_shape = self.shape

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return self.default_value
