from typing import Tuple
from .socket import SOCKET_COLOR_STRING, NodeSocketLogic
from .socket import SOCKET_TYPE_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import Context, Node, NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy.types import Material
import bpy


@socket_type
class NodeSocketLogicTreeNode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLTreeNodeSocket"
    bl_label = "Node"

    default_value: StringProperty(
        name='Node',
        update=update_draw
    )
    # XXX: Remove value property
    value: StringProperty(
        name='Node',
        update=update_draw
    )
    ref_index: IntProperty(default=0)

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            mat_socket = self.node.inputs[self.ref_index]
            tree = mat_socket.default_value
            col = layout.column(align=False)
            if isinstance(tree, Material):
                tree = tree.node_tree
            if tree and not mat_socket.linked_valid:
                col.prop_search(
                    self,
                    "default_value",
                    tree,
                    'nodes',
                    text=''
                )
            elif mat_socket.linked_valid:
                col.label(text=text)
                col.prop(self, 'default_value', text='')
            else:
                col.label(text=self.name)

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)
