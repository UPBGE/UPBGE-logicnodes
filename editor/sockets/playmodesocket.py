from .socket import SOCKET_TYPE_INT_POSITIVE, NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
from .socket import SOCKET_TYPE_INT
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_play_mode_values
from bpy.types import NodeSocket
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicPlayMode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLPlayActionModeSocket"
    bl_label = "Play Mode"

    color = PARAM_INT_SOCKET_COLOR
    valid_sockets = [SOCKET_TYPE_INT, SOCKET_TYPE_INT_POSITIVE]

    value: EnumProperty(
        name='Mode',
        items=_enum_play_mode_values,
        description="The play mode of the action",
        update=update_draw
    )

    def get_unlinked_value(self):
        return self.value

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")
