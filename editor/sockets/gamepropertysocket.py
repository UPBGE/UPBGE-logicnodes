from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from .socket import update_draw
from ...utilities import LOGIC_NODE_IDENTIFIER
from ...utilities import make_valid_name
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicGameProperty(NodeSocket, NodeSocketLogic):
    bl_idname = "NLGamePropertySocket"
    bl_label = "Property"

    value: StringProperty(
        # update=update_tree_code
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit'
        # update=update_tree_code
    )

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        mode = getattr(self.node, 'mode', '0')
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            game_object = None
            game_obj_socket = self.node.inputs[self.ref_index]
            if not game_obj_socket.use_owner:
                game_object = game_obj_socket.value
            else:
                prop_name = f'{LOGIC_NODE_IDENTIFIER}{make_valid_name(tree.name)}'
                for obj in bpy.data.objects:
                    if prop_name in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
                if not game_obj_socket.is_linked and game_object and not mode:
                    row.prop(self, 'use_custom', text='', icon='GREASEPENCIL')
            if game_object or game_obj_socket.is_linked:
                if not game_obj_socket.is_linked and not self.use_custom and mode == '0':
                    game = game_object.game
                    col.prop_search(
                        self,
                        'value',
                        game,
                        'properties',
                        icon='NONE',
                        text=''
                    )
                else:
                    col.prop(self, 'value', text='')
            else:
                col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)