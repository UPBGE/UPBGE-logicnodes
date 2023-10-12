from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from bpy.types import Action
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicAnimation(NodeSocket, NodeSocketLogic):
    bl_idname = "NLAnimationSocket"
    bl_label = "Action"
    value: PointerProperty(
        name='Action',
        type=Action,
        description='Select an Action'
    )
    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text and self.is_linked:
                col.label(text=text)
            col.prop_search(
                self,
                "value",
                bpy.data,
                'actions',
                icon='ACTION',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Action):
            return f'bpy.data.actions.get("{self.value.name}", None)'
