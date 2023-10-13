from .socket import SOCKET_TYPE_SOUND, NodeSocketLogic
from .socket import SOCKET_COLOR_TEXT
from .socket import socket_type
from .socket import update_draw
from bpy.types import Sound
from bpy.types import NodeSocket
from bpy.props import PointerProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicSoundFile(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSoundFileSocket"
    bl_label = "String"
    filepath_value: StringProperty(
        subtype='FILE_PATH'
        # update=update_tree_code
    )
    sound_value: PointerProperty(
        name='Sound',
        type=Sound,
        description='Select a Sound'
        # update=update_tree_code
    )
    use_path: BoolProperty(
        # update=update_tree_code
    )

    color = SOCKET_COLOR_TEXT
    nl_type = SOCKET_TYPE_SOUND

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            row = col.row(align=True)
            text = text if text else 'Sound'
            row.label(text=text)
            row2 = col.row(align=True)
            if self.use_path:
                row2.prop(self, "filepath_value", text='')
            else:
                row2.prop(self, "sound_value", text='')
            row2.operator(
                'logic_nodes.load_sound',
                icon='FILEBROWSER',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.sound_value, Sound):
            return f'bpy.data.sounds.get("{self.sound_value.name}")'
