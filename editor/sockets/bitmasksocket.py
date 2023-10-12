from .socket import NodeSocketLogic
from .socket import PARAM_LIST_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.props import BoolProperty
from bpy.types import NodeSocket


@socket_type
class NodeSocketLogicBitMask(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCollisionMaskSocket"
    bl_label = "Parameter"
    slot_0: BoolProperty(default=True, update=update_draw)
    slot_1: BoolProperty(default=True, update=update_draw)
    slot_2: BoolProperty(default=True, update=update_draw)
    slot_3: BoolProperty(default=True, update=update_draw)
    slot_4: BoolProperty(default=True, update=update_draw)
    slot_5: BoolProperty(default=True, update=update_draw)
    slot_6: BoolProperty(default=True, update=update_draw)
    slot_7: BoolProperty(default=True, update=update_draw)
    slot_8: BoolProperty(default=True, update=update_draw)
    slot_9: BoolProperty(default=True, update=update_draw)
    slot_10: BoolProperty(default=True, update=update_draw)
    slot_11: BoolProperty(default=True, update=update_draw)
    slot_12: BoolProperty(default=True, update=update_draw)
    slot_13: BoolProperty(default=True, update=update_draw)
    slot_14: BoolProperty(default=True, update=update_draw)
    slot_15: BoolProperty(default=True, update=update_draw)

    color = PARAM_LIST_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column(align=True)
            col.scale_y = .8
            row = col.row(align=True)
            row2 = col.row(align=True)
            idx = 0
            while idx < 8:
                row.prop(self, f'slot_{idx}', text='',
                         emboss=True, icon='BLANK1')
                idx += 1
            while idx < 16:
                row2.prop(self, f'slot_{idx}', text='',
                          emboss=True, icon='BLANK1')
                idx += 1

    def get_unlinked_value(self):
        mask = 0
        for slot in range(16):
            if self.get(f'slot_{slot}', 1):
                mask += 1 << slot
        return mask
        # slots = [self.get(f'slot_{idx}', 1) * (2**idx) for idx in range(16)]
        # return sum(slots)
