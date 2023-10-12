from .socket import NodeSocketLogic
from .socket import PARAM_MESH_SOCKET_COLOR
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
    value: PointerProperty(
        name='Mesh',
        type=Mesh
        # update=update_tree_code
    )

    color = PARAM_MESH_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'meshes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Mesh):
            return f'bpy.data.meshes.get("{self.value.name}")'
