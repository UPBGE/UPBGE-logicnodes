from .socket import SOCKET_TYPE_OBJECT, NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import socket_type
from ..filter_types import filter_curves
from bpy.types import NodeSocket
from bpy.types import Curve
from bpy.props import PointerProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicCurve(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCurveObjectSocket"
    bl_label = "Curve"
    value: PointerProperty(
        name='Curve',
        type=Curve,
        poll=filter_curves
    )
    use_owner: BoolProperty(
        name='Use Owner',
        description='Use the owner of this tree'
    )

    nl_color = SOCKET_COLOR_OBJECT
    nl_type = SOCKET_TYPE_OBJECT

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.value is None:
            return "None"
        if self.use_owner:
            return 'game_object'
        return f'scene.objects.get("{self.value.name}", "{self.value.name}")]'
