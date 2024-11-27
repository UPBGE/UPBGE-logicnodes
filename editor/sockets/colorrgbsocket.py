from .socket import SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatVectorProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicColorRGB(NodeSocket, NodeSocketLogic):
    bl_idname = "NLColorSocket"
    bl_label = "Color RGB"

    default_value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=3,
        default=(1.0, 1.0, 1.0),
        update=update_draw
    )
    # XXX: Remove value property
    value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=3,
        default=(1.0, 1.0, 1.0),
        update=update_draw
    )
    nl_color = SOCKET_COLOR_COLOR
    nl_type = SOCKET_TYPE_COLOR
    valid_sockets = [SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR]

    def get_unlinked_value(self):
        v = self.default_value
        return f"mathutils.Vector(({v[0]}, {v[1]}, {v[2]}))"

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text=text if text else 'Color')
            row.prop(self, "default_value", text='')
