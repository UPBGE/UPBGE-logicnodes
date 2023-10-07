from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicFloatFactor(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSocketAlphaFloat"
    bl_label = "Factor"

    value: FloatProperty(
        name='Alpha Value',
        description='Value range from 0 - 1',
        min=0.0,
        max=1.0,
        update=update_draw
    )

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", slider=True, text=text)
        pass

    def get_unlinked_value(self):
        return "{}".format(self.value)
