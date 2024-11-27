from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
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

    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    default_value: EnumProperty(
        name='Mode',
        items=_enum_play_mode_values,
        description="The play mode of the action",
        update=update_draw
    )
    # XXX: Remove value property
    value: EnumProperty(
        name='Mode',
        items=_enum_play_mode_values,
        description="The play mode of the action",
        update=update_draw
    )

    def get_unlinked_value(self):
        return self.default_value

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text="")
