from .socket import SOCKET_TYPE_COLOR, SOCKET_TYPE_VECTOR, NodeSocketLogic
from .socket import SOCKET_COLOR_VECTOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatVectorProperty


@socket_type
class NodeSocketLogicVectorXYZVelocity(NodeSocket, NodeSocketLogic):
    bl_idname = "NLVelocitySocket"
    bl_label = "Velocity"

    default_value: FloatVectorProperty(
        unit='VELOCITY',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_VECTOR
    nl_type = SOCKET_TYPE_VECTOR
    valid_sockets = [SOCKET_TYPE_VECTOR, SOCKET_TYPE_COLOR]

    def get_unlinked_value(self):
        v = self.default_value
        return f"mathutils.Vector(({v[0]}, {v[1]}, {v[2]}))"

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            cont = layout.column(align=True)
            if text != '':
                cont.label(text=text)
            if self.node.width >= 200:
                cont = cont.row(align=True)
            cont.prop(self, "default_value", text='')
