from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ..enum_types import _enum_blend_mode_values
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicBlendMode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLBlendActionMode"
    bl_label = "Blend Mode"
    value: EnumProperty(
        name='Blend Mode',
        items=_enum_blend_mode_values,
        description="The blend mode of the action",
        update=update_draw
    )

    def get_unlinked_value(self):
        return self.value

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
