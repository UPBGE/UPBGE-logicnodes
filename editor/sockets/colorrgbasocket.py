from .socket import NodeSocketLogic
from .socket import PARAM_COLOR_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatVectorProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicColorRGBA(NodeSocket, NodeSocketLogic):
    bl_idname = "NLColorAlphaSocket"
    bl_label = "Float Value"
    value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_draw
    )
    type: StringProperty(default='RGBA')
    nl_color = PARAM_COLOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}, {}))".format(
            self.value[0],
            self.value[1],
            self.value[2],
            self.value[3]
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text=text if text else 'Color')
            row.prop(self, "value", text='')
