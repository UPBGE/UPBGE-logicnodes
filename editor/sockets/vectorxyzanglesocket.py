from ...utilities import DEPRECATED
from .socket import SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_VECTOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatVectorProperty
from bpy.props import FloatProperty


@socket_type
class NodeSocketLogicVectorXYZAngle(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVec3RotationSocket"
    bl_label = "Vector XYZ Angle"

    default_value: FloatVectorProperty(name='Vector', unit='ROTATION', update=update_draw)
    # XXX: Remove value property
    value_x: FloatProperty()
    value_y: FloatProperty()
    value_z: FloatProperty()

    def _update_prop_name(self):
        # XXX: Remove value override
        value_x = getattr(self, 'value_x', DEPRECATED)
        value_y = getattr(self, 'value_y', DEPRECATED)
        value_z = getattr(self, 'value_z', DEPRECATED)
        if value_x is not DEPRECATED:
            self.default_value[0] = value_x
        if value_y is not DEPRECATED:
            self.default_value[1] = value_y
        if value_z is not DEPRECATED:
            self.default_value[2] = value_z

    nl_color = SOCKET_COLOR_VECTOR
    nl_type = SOCKET_TYPE_VECTOR
    valid_sockets = [SOCKET_TYPE_VECTOR, SOCKET_TYPE_COLOR]

    def get_unlinked_value(self):
        v = self.default_value
        return f"mathutils.Vector(({v[0]}, {v[1]}, {v[2]}))"

    def draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            cont = layout.column(align=True)
            if text != '':
                cont.label(text=text)
            if self.node.width >= 200:
                cont = cont.row(align=True)
            cont.prop(self, "default_value", text='')
