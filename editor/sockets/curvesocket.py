from .socket import NodeSocketLogic
from .socket import PARAM_OBJ_SOCKET_COLOR
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
        name='Armature',
        type=Curve,
        poll=filter_curves
        # update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        # update=update_tree_code,
        description='Use the owner of this tree'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

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
            return '"NLO:U_O"'
        return '"NLO:{}"'.format(self.value.name)
