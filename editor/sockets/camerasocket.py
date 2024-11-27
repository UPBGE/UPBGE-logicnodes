from .socket import SOCKET_TYPE_OBJECT, NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import socket_type
from .socket import update_draw
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
    default_value: PointerProperty(
        name='Object',
        type=Object,
        poll=filter_camera,
        update=update_draw
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Object',
        type=Object,
        poll=filter_camera,
        update=update_draw
    )
    use_active: BoolProperty(
        name='Use Active',
        description='Use current active camera',
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
            if not self.use_active:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')
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
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')

    def get_unlinked_value(self):
        if self.use_active:
            return 'self.owner.scene.active_camera'
        if isinstance(self.default_value, Object):
            return f'scene.objects["{self.default_value.name}"]'
