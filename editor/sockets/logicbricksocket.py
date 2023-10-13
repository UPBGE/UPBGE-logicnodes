from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from ...utilities import LOGIC_NODE_IDENTIFIER
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicBrick(NodeSocket, NodeSocketLogic):
    bl_idname = "NLLogicBrickSocket"
    bl_label = "Property"
    value: StringProperty(
        # update=update_tree_code
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit',
        # update=update_tree_code
    )
    brick_type: StringProperty(default='controllers')

    color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def draw(self, context, layout, node, text):
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
                for obj in bpy.data.objects:
                    if f'{LOGIC_NODE_IDENTIFIER}{tree.name}' in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
                if not game_obj_socket.is_linked and game_object:
                    row.prop(self, 'use_custom', text='', icon='GREASEPENCIL')
            if game_object or game_obj_socket.is_linked:
                if not game_obj_socket.is_linked and not self.use_custom:
                    game = game_object.game
                    col.prop_search(
                        self,
                        'value',
                        game,
                        self.brick_type,
                        icon='NONE',
                        text=''
                    )
                else:
                    col.prop(self, 'value', text='')
            else:
                col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)