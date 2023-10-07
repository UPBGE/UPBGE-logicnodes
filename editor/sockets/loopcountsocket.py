from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_loop_count_values
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import EnumProperty
from bpy.props import IntProperty


@socket_type
class NodeSocketLogicLoopCount(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketLoopCount"
    bl_label = "Loop Count"

    value: StringProperty(
        update=update_draw)

    def update_value(self, context):
        current_type = self.value_type
        if current_type == "INFINITE":
            self.value = "-1"
        elif current_type == "ONCE":
            self.value = "1"
        elif current_type == "CUSTOM":
            self.value = '{}'.format(int(self.integer_editor) - 1)
    value_type: EnumProperty(
        name='Loop Count',
        items=_enum_loop_count_values,
        update=update_value
    )
    integer_editor: IntProperty(
        update=update_value,
        min=1,
        default=1,
        description=(
            'How many times the sound should '
            'be repeated when the condition is TRUE'
        )
    )

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            current_type = self.value_type
            if (current_type == "INFINITE") or (current_type == "ONCE"):
                layout.label(text=text)
                layout.prop(self, "value_type", text="")
            else:
                layout.prop(self, "integer_editor", text="")
                layout.prop(self, "value_type", text="")

    def get_unlinked_value(self):
        current_type = self.value_type
        if current_type == "INFINITE":
            return "-1"
        if current_type == "ONCE":
            return "0"
        return '{}'.format(self.value)
