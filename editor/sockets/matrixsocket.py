from .socket import SOCKET_TYPE_MATRIX, NodeSocketLogic
from .socket import SOCKET_TYPE_VECTOR
from .socket import SOCKET_COLOR_VECTOR
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_matrix_dimensions
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import EnumProperty


@socket_type
class NodeSocketLogicMatrix(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicMatrix"
    bl_label = "Matrix"

    dimensions: EnumProperty(items=_enum_matrix_dimensions, name='Dimensions')

    value_xx: FloatProperty(default=0)
    value_xy: FloatProperty(default=0)
    value_xz: FloatProperty(default=0)
    value_xw: FloatProperty(default=0)

    value_yx: FloatProperty(default=0)
    value_yy: FloatProperty(default=0)
    value_yz: FloatProperty(default=0)
    value_yw: FloatProperty(default=0)

    value_zx: FloatProperty(default=0)
    value_zy: FloatProperty(default=0)
    value_zz: FloatProperty(default=0)
    value_zw: FloatProperty(default=0)

    value_wx: FloatProperty(default=0)
    value_wy: FloatProperty(default=0)
    value_wz: FloatProperty(default=0)
    value_ww: FloatProperty(default=0)

    nl_color = SOCKET_COLOR_VECTOR
    nl_type = SOCKET_TYPE_MATRIX
    valid_sockets = [SOCKET_TYPE_MATRIX, SOCKET_TYPE_VECTOR]

    def get_unlinked_value(self):
        return "mathutils.Matrix(([{}, {}, {}, {}], [{}, {}, {}, {}], [{}, {}, {}, {}], [{}, {}, {}, {}]))".format(
            self.value_xx,
            self.value_xy,
            self.value_xz,
            self.value_xw,
            self.value_yx,
            self.value_yy,
            self.value_yz,
            self.value_yw,
            self.value_zx,
            self.value_zy,
            self.value_zz,
            self.value_zw,
            self.value_wx,
            self.value_wy,
            self.value_wz,
            self.value_ww
        ) if int(self.dimensions) > 1 else "mathutils.Matrix(([{}, {}, {}], [{}, {}, {}], [{}, {}, {}]))".format(
            self.value_xx,
            self.value_xy,
            self.value_xz,
            self.value_yx,
            self.value_yy,
            self.value_yz,
            self.value_zx,
            self.value_zy,
            self.value_zz
        )

    def _draw(self, context, layout, node, text):
        dim = int(self.dimensions) > 1
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            col.prop(self, 'dimensions', text='')
            matrix = col.column(align=True)
            cont = matrix.row(align=True)
            cont.prop(self, "value_xx", text='')
            cont.prop(self, "value_xy", text='')
            cont.prop(self, "value_xz", text='')
            if dim:
                cont.prop(self, "value_xw", text='')
            cont = matrix.row(align=True)
            cont.prop(self, "value_yx", text='')
            cont.prop(self, "value_yy", text='')
            cont.prop(self, "value_yz", text='')
            if dim:
                cont.prop(self, "value_yw", text='')
            cont = matrix.row(align=True)
            cont.prop(self, "value_zx", text='')
            cont.prop(self, "value_zy", text='')
            cont.prop(self, "value_zz", text='')
            if dim:
                cont.prop(self, "value_zw", text='')
                cont = matrix.row(align=True)
                cont.prop(self, "value_wx", text='')
                cont.prop(self, "value_wy", text='')
                cont.prop(self, "value_wz", text='')
                cont.prop(self, "value_ww", text='')
