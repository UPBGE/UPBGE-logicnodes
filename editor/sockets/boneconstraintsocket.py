from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from ...utilities import LOGIC_NODE_IDENTIFIER
from ...utilities import make_valid_name
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicBoneConstraint(NodeSocket, NodeSocketLogic):
    bl_idname = "NLBoneConstraintSocket"
    bl_label = "Bone Constraint"
    default_value: StringProperty(name='Bone Constraint', update=update_draw)
    # XXX: Remove value property
    value: StringProperty(name='Bone Constraint', update=update_draw)
    ref_index: IntProperty(default=0)

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text='Constraint Name')
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            bone = None
            bone_socket = self.node.inputs[self.ref_index]
            armature_socket = self.node.inputs[bone_socket.ref_index]
            armature = None
            if not armature_socket.use_owner:
                armature = armature_socket.default_value
                if bone_socket.default_value and armature:
                    bone = armature.pose.bones.get(bone_socket.default_value)
            elif bone_socket.default_value:
                for obj in bpy.data.objects:
                    if f'{LOGIC_NODE_IDENTIFIER}{make_valid_name(tree.name)}' in obj.game.properties:
                        armature = obj
                        bone = armature.pose.bones.get(bone_socket.default_value)
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
            if bone:
                if not bone_socket.linked_valid and not armature_socket.linked_valid:
                    col.prop_search(
                        self,
                        'default_value',
                        bone,
                        'constraints',
                        text=''
                    )
                    return
            if (bone or bone_socket.linked_valid) and (armature or armature_socket.linked_valid):
                col.prop(self, 'default_value', text='')
            else:
                col.label(text='No Bone!', icon='ERROR')

    def get_unlinked_value(self):
        return repr(self.default_value)
