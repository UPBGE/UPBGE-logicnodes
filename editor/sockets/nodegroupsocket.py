from .socket import NodeSocketLogic
from .socket import PARAM_SCENE_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeTree
from bpy.types import NodeSocket
from bpy.props import PointerProperty
from ..filter_types import filter_node_groups
import bpy


@socket_type
class NodeSocketLogicNodeGroup(NodeSocket, NodeSocketLogic):
    bl_idname = "NLNodeGroupSocket"
    bl_label = "Node Tree"
    value: PointerProperty(
        name='Node Tree',
        type=NodeTree,
        poll=filter_node_groups
        # update=update_tree_code
    )

    color = PARAM_SCENE_SOCKET_COLOR

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
                'node_groups',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, NodeTree):
            return '"{}"'.format(self.value.name)
