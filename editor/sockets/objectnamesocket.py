from .socket import NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import SOCKET_TYPE_STRING
from .socket import socket_type
from bpy.types import Object
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicObjectName(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGameObjectNameSocket"
    bl_label = "Object"
    value: PointerProperty(
        name='Object',
        type=Object
    )
    deprecated = True

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.context.scene,
                'objects',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Object):
            return repr(self.value.name)
