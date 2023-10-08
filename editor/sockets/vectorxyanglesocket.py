from .socket import NodeSocketLogic
from .socket import PARAM_VECTOR_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVectorXYAngle(NodeSocket, NodeSocketLogic):
    bl_idname = "NLAngleLimitSocket"
    bl_label = "Float Value"

    value_x: FloatProperty(
        default=0,
        unit='ROTATION',
        update=update_draw
    )
    value_y: FloatProperty(
        default=0,
        unit='ROTATION',
        update=update_draw
    )
    title: StringProperty(default='')

    color = PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}))".format(self.value_x, self.value_y)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            if text != '':
                column.label(text=text)
            row = column.row(align=True)
            row.prop(self, "value_x", text='')
            row.prop(self, "value_y", text='')
