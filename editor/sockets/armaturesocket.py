from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import SOCKET_TYPE_ARMATURE
from .socket import socket_type
from .socket import update_draw
from ..filter_types import filter_armatures
from bpy.types import NodeSocket
from bpy.types import Armature
from bpy.props import PointerProperty
from bpy.props import BoolProperty
import bpy


# @socket_type
# class NodeSocketLogicArmature(NodeSocketInterfaceLogic):
#     bl_socket_idname = 'NLArmatureObjectSocket'


@socket_type
class NodeSocketLogicArmature(NodeSocket, NodeSocketLogic):
    bl_idname = "NLArmatureObjectSocket"
    bl_label = "Armature"

    default_value: PointerProperty(
        name='Armature',
        type=Armature,
        update=update_draw,
        poll=filter_armatures
    )
    use_owner: BoolProperty(
        name='Use Owner',
        description='Use the owner of this tree'
    )

    nl_color = SOCKET_COLOR_OBJECT
    nl_type = SOCKET_TYPE_ARMATURE

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
        if self.use_owner:
            return 'game_object'
        if self.default_value is not None and isinstance(self.default_value.data, Armature):
            return f'scene.objects.get("{self.default_value.name}", "{self.default_value.name}")'
