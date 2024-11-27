from .socket import SOCKET_TYPE_MATERIAL, NodeSocketLogic
from .socket import SOCKET_COLOR_MATERIAL
from .socket import socket_type
from .socket import update_draw
from bpy.types import Material
from bpy.types import NodeSocket
from bpy.props import PointerProperty
from ..filter_types import filter_materials
import bpy


@socket_type
class NodeSocketLogicMaterial(NodeSocket, NodeSocketLogic):
    bl_idname = "NLMaterialSocket"
    bl_label = "Material"
    default_value: PointerProperty(
        name='Material',
        type=Material,
        poll=filter_materials
        # update=update_tree_code
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Material',
        type=Material,
        poll=filter_materials
        # update=update_tree_code
    )

    nl_color = SOCKET_COLOR_MATERIAL
    nl_type = SOCKET_TYPE_MATERIAL

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.linked_valid:
                col.label(text=self.name)
            col.prop_search(
                self,
                'default_value',
                bpy.data,
                'materials',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, bpy.types.Material):
            return f'bpy.data.materials.get("{self.default_value.name}")'
