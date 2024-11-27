from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .objectsocket import NodeSocketLogicObject
from .socket import socket_type
from .socket import update_draw
from ...utilities import LOGIC_NODE_IDENTIFIER
from ...utilities import make_valid_name
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicConstraint(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicConstraint"
    bl_label = "Constraint"
    default_value: StringProperty(name='Bone Constraint', update=update_draw)
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(name='Free Edit')

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        mode = getattr(self.node, 'mode', '0')
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            data_block = None
            data_block_socket = self.node.inputs[self.ref_index]
            if not getattr(data_block_socket, 'use_owner', False):
                data_block = data_block_socket.default_value
            elif isinstance(data_block_socket, NodeSocketLogicObject):
                const_name = f'{LOGIC_NODE_IDENTIFIER}{make_valid_name(tree.name)}'
                for obj in bpy.data.objects:
                    if const_name in obj.constraints:
                        data_block = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
                if not data_block_socket.linked_valid and data_block and not mode:
                    row.prop(self, 'use_custom', text='', icon='GREASEPENCIL')
            if data_block or data_block_socket.linked_valid:
                if not data_block_socket.linked_valid and not self.use_custom and mode == '0':
                    col.prop_search(
                        self,
                        'default_value',
                        data_block,
                        'constraints',
                        icon='NONE',
                        text=''
                    )
                else:
                    col.prop(self, 'default_value', text='')
            else:
                col.prop(self, 'default_value', text='')

    def get_unlinked_value(self):
        return repr(self.default_value)
