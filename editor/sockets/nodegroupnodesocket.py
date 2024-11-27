from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicNodeGroupNode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLNodeGroupNodeSocket"
    bl_label = "Tree Node"

    default_value: StringProperty(
        name='Tree Node',
        update=update_draw
    )
    # XXX: Remove value property
    value: StringProperty(
        name='Tree Node',
        update=update_draw
    )
    ref_index: IntProperty(default=0)

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            tree_socket = self.node.inputs[self.ref_index]
            tree = tree_socket.default_value
            col = layout.column(align=False)
            if tree and not tree_socket.linked_valid:
                col.prop_search(
                    self,
                    "default_value",
                    bpy.data.node_groups[tree.name],
                    'nodes',
                    text=''
                )
            elif tree_socket.linked_valid:
                col.label(text=text)
                col.prop(self, 'default_value', text='')
            else:
                col.label(text=self.name)

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)
