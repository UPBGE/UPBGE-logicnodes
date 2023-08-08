from .socket import NodeSocketLogic
from .socket import PARAM_OBJ_SOCKET_COLOR
from .socket import socket_type
from ..filter_types import filter_speaker
from bpy.types import NodeSocket
from bpy.types import Object
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicSpeaker(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSpeakerSocket"
    bl_label = "Camera"
    value: PointerProperty(
        name='Object',
        type=Object,
        poll=filter_speaker
        # update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            row = col.row()
            if self.name:
                row.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.context.scene,
                'objects',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Object):
            return '"NLO:{}"'.format(self.value.name)
