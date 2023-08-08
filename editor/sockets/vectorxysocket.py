from .socket import NodeSocketLogic
from .socket import PARAM_VECTOR_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVectorXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVec2FieldSocket"
    bl_label = "Float Value"
    value_x: FloatProperty(default=0, update=update_draw)
    value_y: FloatProperty(default=0, update=update_draw)
    title: StringProperty(default='')
    type: StringProperty(default='VECTOR')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

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
