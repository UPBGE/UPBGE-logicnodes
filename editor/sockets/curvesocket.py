from .socket import SOCKET_TYPE_OBJECT, NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import socket_type
from .socket import update_draw
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
    default_value: PointerProperty(
        name='Curve',
        type=Curve,
        poll=filter_curves,
        update=update_draw
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Curve',
        type=Curve,
        poll=filter_curves,
        update=update_draw
    )
    use_owner: BoolProperty(
        name='Use Owner',
        description='Use the owner of this tree',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_OBJECT
    nl_type = SOCKET_TYPE_OBJECT

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
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
                    'default_value',
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
        if self.default_value is None:
            return "None"
        if self.use_owner:
            return 'game_object'
        return f'scene.objects.get("{self.default_value.name}", "{self.default_value.name}")'
