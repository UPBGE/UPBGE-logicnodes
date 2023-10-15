from .socket import SOCKET_TYPE_NODETREE, NodeSocketLogic
from .socket import SOCKET_COLOR_GEOTREE
from .socket import socket_type
from bpy.types import GeometryNodeTree
from bpy.types import NodeSocket
from bpy.props import PointerProperty
from ..filter_types import filter_geometry_nodes
import bpy


@socket_type
class NodeSocketLogicGeometryNodeTree(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGeomNodeTreeSocket"
    bl_label = "Geometry Node Tree"
    value: PointerProperty(
        name='Geometry Node Tree',
        type=GeometryNodeTree,
        poll=filter_geometry_nodes
    )

    nl_color = SOCKET_COLOR_GEOTREE
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
        if isinstance(self.value, GeometryNodeTree):
            return f'bpy.data.node_groups["{self.value.name}"]'
        return None
