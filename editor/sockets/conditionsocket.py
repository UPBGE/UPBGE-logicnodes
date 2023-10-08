from .socket import NodeSocketLogic
from .socket import CONDITION_SOCKET_COLOR
from .socket import SOCKET_TYPE_BOOL
from .socket import SOCKET_TYPE_CONDITION
from .socket import socket_type
from .socket import update_draw
from bpy.props import StringProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicCondition(NodeSocket, NodeSocketLogic):
    bl_idname = "NLConditionSocket"
    bl_label = "Condition"
    nl_type = SOCKET_TYPE_CONDITION
    valid_sockets = [SOCKET_TYPE_CONDITION, SOCKET_TYPE_BOOL]
    description = StringProperty(default='Execution Condition')
    default_value: StringProperty(
        name='Condition',
        default="None"
    )

    color = CONDITION_SOCKET_COLOR

    def shape_setup(self):
        self.display_shape = self.shape

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return self.default_value
