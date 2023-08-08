from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicTreeNode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLTreeNodeSocket"
    bl_label = "Tree Node"
    value: StringProperty(
        name='Tree Node',
        update=update_draw
    )
    ref_index: IntProperty(default=0)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            mat_socket = self.node.inputs[self.ref_index]
            mat = mat_socket.value
            col = layout.column(align=False)
            if mat and not mat_socket.is_linked:
                col.prop_search(
                    self,
                    "value",
                    bpy.data.materials[mat.name].node_tree,
                    'nodes',
                    text=''
                )
            elif mat_socket.is_linked:
                col.label(text=text)
                col.prop(self, 'value', text='')
            else:
                col.label(text=self.name)

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)
