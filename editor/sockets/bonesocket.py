from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ...utilities import LOGIC_NODE_IDENTIFIER
from ...utilities import make_valid_name
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicBone(NodeSocket, NodeSocketLogic):
    bl_idname = "NLArmatureBoneSocket"
    bl_label = "Property"
    value: StringProperty()
    ref_index: IntProperty(default=0)

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text='Bone Name')
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
                    if f'{LOGIC_NODE_IDENTIFIER}{make_valid_name(tree.name)}' in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
            if game_object and isinstance(game_object.data, bpy.types.Armature):
                if not game_obj_socket.is_linked:
                    col.prop_search(
                        self,
                        'value',
                        game_object.pose,
                        'bones',
                        icon='NONE',
                        text=''
                    )
                    return
            if game_obj_socket.is_linked:
                col.prop(self, 'value', text='')
            else:
                col.label(text='No Armature!', icon='ERROR')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)
