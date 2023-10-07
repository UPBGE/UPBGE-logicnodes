from .socket import NodeSocketLogic
from .socket import PARAM_GEOMTREE_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
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

    color = PARAM_GEOMTREE_SOCKET_COLOR

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
            return '"{}"'.format(self.value.name)
