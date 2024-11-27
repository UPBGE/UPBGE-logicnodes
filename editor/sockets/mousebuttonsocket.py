from .socket import SOCKET_TYPE_INT, NodeSocketLogic
from .socket import SOCKET_COLOR_INTEGER
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_mouse_buttons
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicMouseButton(NodeSocket, NodeSocketLogic):
    bl_idname = "NLMouseButtonSocket"
    bl_label = "Mouse Button"

    default_value: EnumProperty(
        name='Button',
        items=_enum_mouse_buttons, default="bge.events.LEFTMOUSE",
        update=update_draw
    )
    # XXX: Remove value property
    value: EnumProperty(
        name='Button',
        items=_enum_mouse_buttons, default="bge.events.LEFTMOUSE",
        update=update_draw
    )
    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def get_unlinked_value(self):
        return self.default_value

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text="")
