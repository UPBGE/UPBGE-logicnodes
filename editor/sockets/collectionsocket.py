from .socket import SOCKET_TYPE_COLLECTION, NodeSocketLogic
from .socket import SOCKET_COLOR_COLLECTION
from .socket import socket_type
from bpy.types import Collection
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicCollection(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCollectionSocket"
    bl_label = "Collection"
    value: PointerProperty(
        name='Collection',
        type=Collection,
        description=(
            'Select a Collection. '
            'Objects in that collection will be used for the node'
        )
        # update=update_tree_code
    )

    nl_color = SOCKET_COLOR_COLLECTION
    nl_type = SOCKET_TYPE_COLLECTION

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=text)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'collections',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, Collection):
            return f'bpy.data.collections.get("{self.value.name}")'
