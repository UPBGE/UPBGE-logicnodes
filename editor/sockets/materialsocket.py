from .socket import NodeSocketLogic
from .socket import PARAM_MAT_SOCKET_COLOR
from .socket import socket_type
from bpy.types import Material
from bpy.types import NodeSocket
from bpy.props import PointerProperty
from ..filter_types import filter_materials
import bpy


@socket_type
class NodeSocketLogicMaterial(NodeSocket, NodeSocketLogic):
    bl_idname = "NLMaterialSocket"
    bl_label = "Material"
    value: PointerProperty(
        name='Material',
        type=Material,
        poll=filter_materials
        # update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_MAT_SOCKET_COLOR

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
                'materials',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Material):
            return '"{}"'.format(self.value.name)
