from .socket import SOCKET_TYPE_OBJECT, NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import socket_type
from .socket import update_draw
from ..filter_types import filter_navmesh
from bpy.types import NodeSocket
from bpy.types import Object
from bpy.props import PointerProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicNavMesh(NodeSocket, NodeSocketLogic):
    bl_idname = "NLNavMeshSocket"
    bl_label = "Object"
    value: PointerProperty(
        name='Object',
        type=Object,
        poll=filter_navmesh
        # update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        # update=update_tree_code,
        description='Use the owner of this tree'
    )

    color = SOCKET_COLOR_OBJECT
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
        if self.use_owner:
            return 'game_object'
        if isinstance(self.value, Object):
            return f'scene.objects[{self.value.name}]'