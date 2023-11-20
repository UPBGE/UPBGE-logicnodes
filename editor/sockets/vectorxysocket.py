from ...utilities import DEPRECATED
from .socket import SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_VECTOR
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import FloatVectorProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVectorXY(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVec2FieldSocket"
    bl_label = "Vector XY"

    default_value: FloatVectorProperty(name='Vector', size=2)
    title: StringProperty(default='')
    # XXX: Remove value property
    value_x: FloatProperty()
    value_y: FloatProperty()

    def _update_prop_name(self):
        # XXX: Remove value override
        value_x = getattr(self, 'value_x', DEPRECATED)
        value_y = getattr(self, 'value_y', DEPRECATED)
        if value_x is not DEPRECATED:
            self.default_value[0] = value_x
        if value_y is not DEPRECATED:
            self.default_value[1] = value_y

    nl_color = SOCKET_COLOR_VECTOR
    nl_type = SOCKET_TYPE_VECTOR
    valid_sockets = [SOCKET_TYPE_VECTOR, SOCKET_TYPE_COLOR]

    def get_unlinked_value(self):
        v = self.default_value
        return f"mathutils.Vector(({v[0]}, {v[1]}))"

    def draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            if text != '':
                column.label(text=text)
            row = column.row(align=True)
            row.prop(self, 'default_value', text='')
