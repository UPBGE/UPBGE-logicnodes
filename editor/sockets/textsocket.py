from .socket import SOCKET_TYPE_TEXT, NodeSocketLogic
from .socket import SOCKET_COLOR_TEXT
from .socket import socket_type
from .socket import update_draw
from ..filter_types import filter_texts
from bpy.types import Text
from bpy.types import NodeSocket
from bpy.props import PointerProperty
import bpy


@socket_type
class NodeSocketLogicText(NodeSocket, NodeSocketLogic):
    bl_idname = "NLTextIDSocket"
    bl_label = "Text"
    default_value: PointerProperty(
        name='Text',
        type=Text,
        poll=filter_texts
        # update=update_tree_code
    )
    # XXX: Remove value property
    value: PointerProperty(
        name='Text',
        type=Text,
        poll=filter_texts
        # update=update_tree_code
    )

    nl_color = SOCKET_COLOR_TEXT
    nl_type = SOCKET_TYPE_TEXT

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
                'texts',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, Text):
            return f'bpy.data.texts["{self.default_value.name}"]'
