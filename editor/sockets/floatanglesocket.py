from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicFloatAngle(NodeSocket, NodeSocketLogic):
    bl_idname = "NLFloatAngleSocket"
    bl_label = "Float Value"

    value: FloatProperty(
        default=0,
        update=update_draw,
        unit='ROTATION'
    )
    color = PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
