from .socket import NodeSocketLogic
from .socket import PARAM_INT_SOCKET_COLOR
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

    value: EnumProperty(
        name='Button',
        items=_enum_mouse_buttons, default="bge.events.LEFTMOUSE",
        update=update_draw
    )
    color = PARAM_INT_SOCKET_COLOR

    def get_unlinked_value(self):
        return self.value

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")
