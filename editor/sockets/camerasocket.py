from .socket import NodeSocketLogic
from .socket import PARAM_OBJ_SOCKET_COLOR
from .socket import socket_type
from ..filter_types import filter_camera
from bpy.types import NodeSocket
from bpy.types import Object
from bpy.props import PointerProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicCamera(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCameraSocket"
    bl_label = "Camera"
    value: PointerProperty(
        name='Object',
        type=Object,
        poll=filter_camera
        # update=update_tree_code
    )
    use_active: BoolProperty(
        name='Use Active',
        # update=update_tree_code,
        description='Use current active camera'
    )

    color = PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_active:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')
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
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')

    def get_unlinked_value(self):
        if self.use_active:
            return 'self.owner.scene.active_camera'
        if isinstance(self.value, Object):
            return '"NLO:{}"'.format(self.value.name)
