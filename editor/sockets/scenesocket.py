from .socket import SOCKET_TYPE_SCENE, NodeSocketLogic
from .socket import SOCKET_COLOR_MATERIAL
from .socket import socket_type
from .socket import update_draw
from bpy.types import Scene
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicScene(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSceneSocket"
    bl_label = "Scene"
    default_value: PointerProperty(
        name='Scene',
        type=Scene
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Scene',
        type=Scene
    )

    nl_color = SOCKET_COLOR_MATERIAL
    nl_type = SOCKET_TYPE_SCENE

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.linked_valid:
                col.label(text=self.name)
            col.prop_search(
                self,
                'default_value',
                bpy.data,
                'scenes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, Scene):
            return f'bpy.data.scenes.get("{self.default_value.name}")'
