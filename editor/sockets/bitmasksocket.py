from .socket import SOCKET_COLOR_INTEGER, SOCKET_TYPE_INT, NodeSocketLogic
from .socket import socket_type
from bpy.props import BoolVectorProperty
from bpy.props import IntProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicBitMask(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCollisionMaskSocket"
    bl_label = "Bitmask"
    default_value: BoolVectorProperty(
        size=16,
        default=[True for x in range(16)],
        name='Mask',
        subtype='LAYER_MEMBER'  # XXX: Reactivate if fixed
    )
    selected_bit: IntProperty()

    nl_color = SOCKET_COLOR_INTEGER
    nl_type = SOCKET_TYPE_INT

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            layout.prop(self, 'default_value', text='', icon='BLANK1')

    def get_unlinked_value(self):
        mask = 0
        for slot in range(16):
            if self.default_value[slot]:
                mask += 1 << slot
        return mask
