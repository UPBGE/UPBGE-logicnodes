from .socket import SOCKET_TYPE_COLLECTION, NodeSocketLogic
from .socket import SOCKET_COLOR_COLLECTION
from .socket import socket_type
from .socket import update_draw
from bpy.types import Collection
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicCollection(NodeSocket, NodeSocketLogic):
    bl_idname = "NLCollectionSocket"
    bl_label = "Collection"
    default_value: PointerProperty(
        name='Collection',
        type=Collection,
        update=update_draw
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Collection',
        type=Collection,
        update=update_draw
    )

    nl_color = SOCKET_COLOR_COLLECTION
    nl_type = SOCKET_TYPE_COLLECTION

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.linked_valid:
                col.label(text=text)
            col.prop_search(
                self,
                'default_value',
                bpy.data,
                'collections',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, Collection):
            return f'bpy.data.collections.get("{self.default_value.name}")'
