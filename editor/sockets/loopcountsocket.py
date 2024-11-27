from .socket import SOCKET_COLOR_INTEGER, SOCKET_TYPE_INT, NodeSocketLogic
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import EnumProperty
from bpy.props import IntProperty


_loops = [
    (
        "0",
        "Once",
        (
            'Play once when condition is TRUE, then wait for '
            'the condition to become TRUE again to play it again.'
        )
    ), (
        "-1",
        "Loop",
        "When condition is TRUE, start repeating the sound until stopped."
    ), (
        "1",
        "Times",
        "When the condition it TRUE, play the sound N times"
    )
]

@socket_type
class NodeSocketLogicLoopCount(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketLoopCount"
    bl_label = "Loop Count"
    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    default_value: IntProperty(update=update_draw)
    # XXX: Remove value property
    value: IntProperty(update=update_draw)

    def update_value(self, context):
        self.default_value = int(self.value_type) if int(self.value_type) != 1 else self.integer_editor - 1

    value_type: EnumProperty(
        name='Loop Count',
        items=_loops,
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

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            current_type = self.value_type
            layout.prop(self, "value_type", text="")
            if current_type == "1":
                layout.prop(self, "integer_editor", text="")

    def get_unlinked_value(self):
        current_type = self.value_type
        if current_type == "INFINITE":
            return -1
        if current_type == "ONCE":
            return 0
        return self.default_value
