from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_OBJECT
from .socket import SOCKET_TYPE_OBJECT
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.types import Object
from bpy.props import PointerProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicObject(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGameObjectSocket"
    bl_label = "Object"
    nl_type = SOCKET_TYPE_OBJECT
    nl_color = SOCKET_COLOR_OBJECT

    default_value: PointerProperty(name='Object', type=Object)

    # XXX: Remove value property
    value: PointerProperty(name='Object', type=Object)

    use_owner: BoolProperty(
        name='Use Owner',
        description='Use the owner of this tree'
    )

    allow_owner: BoolProperty(default=True)

    def is_scene_logic(self):
        if not hasattr(self.node, 'tree'):
            return False
        return self.node.tree is bpy.context.scene.get(
            'custom_mainloop_tree',
            None
        )

    def _draw(self, context, layout, node, text):
        scene_logic = self.is_scene_logic()
        if self.link_limit != 1:
            layout.label(text=self.name)
            return
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            if not self.use_owner or scene_logic:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                if self.allow_owner and not scene_logic:
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
                if self.allow_owner:
                    row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.use_owner and not self.is_scene_logic():
            return 'game_object'
        if isinstance(self.default_value, bpy.types.Object):
            return f'scene.objects.get("{self.default_value.name}", "{self.default_value.name}")'