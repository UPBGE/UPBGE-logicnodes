from .socket import NodeSocketLogic
from .socket import PARAM_MAT_SOCKET_COLOR
from .socket import socket_type
from bpy.types import Scene
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicScene(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSceneSocket"
    bl_label = "Scene"
    value: PointerProperty(
        name='Scene',
        type=Scene
    )

    def draw_color(self, context, node):
        return PARAM_MAT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'scenes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Scene):
            return '"{}"'.format(self.value.name)
