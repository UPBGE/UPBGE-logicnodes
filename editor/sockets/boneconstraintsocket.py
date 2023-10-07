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
class NodeSocketLogicBoneConstraint(NodeSocket, NodeSocketLogic):
    bl_idname = "NLBoneConstraintSocket"
    bl_label = "Property"
    value: StringProperty()
    ref_index: IntProperty(default=0)

    color = PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
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
                armature = armature_socket.value
                if bone_socket.value and armature:
                    bone = armature.pose.bones.get(bone_socket.value)
            elif bone_socket.value:
                for obj in bpy.data.objects:
                    if f'{LOGIC_NODE_IDENTIFIER}{make_valid_name(tree.name)}' in obj.game.properties:
                        armature = obj
                        bone = armature.pose.bones.get(bone_socket.value)
                        break
            # if not armature_socket.is_linked and bone_socket.value and armature:
            #     armature = armature_socket.value
            if self.name:
                row = col.row()
                row.label(text=self.name)
            if bone:
                if not bone_socket.is_linked and not armature_socket.is_linked:
                    col.prop_search(
                        self,
                        'value',
                        bone,
                        'constraints',
                        text=''
                    )
                    return
            if (bone or bone_socket.is_linked) and (armature or armature_socket.is_linked):
                col.prop(self, 'value', text='')
            else:
                col.label(text='No Bone!', icon='ERROR')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)
