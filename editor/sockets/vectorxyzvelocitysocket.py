from .socket import NodeSocketLogic
from .socket import PARAM_VECTOR_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty


@socket_type
class NodeSocketLogicVectorXYZVelocity(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVelocitySocket"
    bl_label = "Float Value"

    type: StringProperty(default='VECTOR')
    value_x: FloatProperty(
        default=0,
        unit='VELOCITY',
        update=update_draw
    )
    value_y: FloatProperty(
        default=0,
        unit='VELOCITY',
        update=update_draw
    )
    value_z: FloatProperty(
        default=0,
        unit='VELOCITY',
        update=update_draw
    )

    color = PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}))".format(
            self.value_x,
            self.value_y,
            self.value_z
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            cont = layout.column(align=True)
            if text != '':
                cont.label(text=text)
            if self.node.width >= 200:
                cont = cont.row(align=True)
            cont.prop(self, "value_x", text='X')
            cont.prop(self, "value_y", text='Y')
            cont.prop(self, "value_z", text='Z')
