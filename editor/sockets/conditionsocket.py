from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_CONDITION
from .socket import SOCKET_TYPE_BOOL
from .socket import SOCKET_TYPE_CONDITION
from .socket import socket_type
from bpy.props import BoolProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicCondition(NodeSocket, NodeSocketLogic):
    bl_idname = "NLConditionSocket"
    bl_label = "Condition"
    nl_type = SOCKET_TYPE_CONDITION
    valid_sockets = [SOCKET_TYPE_CONDITION, SOCKET_TYPE_BOOL]

    default_value: BoolProperty(
        name='Condition'
    )
    # XXX: Remove value property
    value: BoolProperty(
        name='Condition'
    )
    show_prop: BoolProperty()

    nl_color = SOCKET_COLOR_CONDITION

    def shape_setup(self):
        self.display_shape = self.shape

    def _draw(self, context, layout, node, text):
        if self.show_prop and not self.is_output and not self.linked_valid:
            row = layout.row()
            row.prop(self, 'default_value', text=text)
        else:
            layout.label(text=text)

    def get_unlinked_value(self):
        return self.default_value
