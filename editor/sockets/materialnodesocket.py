from .socket import SOCKET_COLOR_STRING, NodeSocketLogic
from .socket import SOCKET_TYPE_STRING
from .socket import socket_type
from .socket import update_draw
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicMaterialNode(NodeSocket, NodeSocketLogic):
    bl_idname = "NLTreeNodeSocket"
    bl_label = "Material Node"

    value: StringProperty(
        name='Material Node',
        update=update_draw
    )
    ref_index: IntProperty(default=0)

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

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
