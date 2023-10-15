from .socket import SOCKET_TYPE_NODETREE, NodeSocketLogic
from .socket import SOCKET_COLOR_SCENE
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

    nl_color = SOCKET_COLOR_SCENE
    nl_type = SOCKET_TYPE_NODETREE

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
            return f'bpy.data.node_groups["{self.value.name}"]'
