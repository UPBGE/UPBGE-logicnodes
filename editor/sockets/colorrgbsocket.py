from .socket import SOCKET_TYPE_COLOR, NodeSocketLogic
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

    value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=3,
        default=(1.0, 1.0, 1.0),
        update=update_draw
    )
    nl_color = SOCKET_COLOR_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}))".format(
            self.value[0],
            self.value[1],
            self.value[2]
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text=text if text else 'Color')
            row.prop(self, "value", text='')
