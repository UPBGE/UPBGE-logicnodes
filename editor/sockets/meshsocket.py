from .socket import SOCKET_TYPE_MESH, NodeSocketLogic
from .socket import SOCKET_COLOR_MESH
from .socket import socket_type
from .socket import update_draw
from bpy.types import Mesh
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicMesh(NodeSocket, NodeSocketLogic):
    bl_idname = "NLMeshSocket"
    bl_label = "Mesh"
    default_value: PointerProperty(
        name='Mesh',
        type=Mesh
        # update=update_tree_code
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Mesh',
        type=Mesh
        # update=update_tree_code
    )

    nl_color = SOCKET_COLOR_MESH
    nl_type = SOCKET_TYPE_MESH

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.linked_valid:
                col.label(text=self.name)
            col.prop_search(
                self,
                'default_value',
                bpy.data,
                'meshes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, Mesh):
            return f'bpy.data.meshes.get("{self.default_value.name}")'
