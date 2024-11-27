from ...utilities import DEPRECATED
from .socket import SOCKET_TYPE_SOUND, NodeSocketLogic
from .socket import SOCKET_COLOR_TEXT
from .socket import socket_type
from .socket import update_draw
from bpy.types import Sound
from bpy.types import NodeSocket
from bpy.props import PointerProperty

@socket_type
class NodeSocketLogicSoundFile(NodeSocket, NodeSocketLogic):
    bl_idname = "NLSoundFileSocket"
    bl_label = "Sound"

    default_value: PointerProperty(
        name='Sound',
        type=Sound,
        description='Select a Sound',
        update=update_draw
    )
    # XXX: Remove sound_value property
    sound_value: PointerProperty(
        name='Sound',
        type=Sound,
        description='Select a Sound',
        update=update_draw
    )

    nl_color = SOCKET_COLOR_TEXT
    nl_type = SOCKET_TYPE_SOUND

    def _update_prop_name(self):
        sval = getattr(self, 'sound_value', DEPRECATED)
        if sval is not DEPRECATED:
            self.default_value = sval

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            col = layout.column()
            row = col.row(align=True)
            text = text if text else 'Sound'
            row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "default_value", text='')
            row2.operator(
                'logic_nodes.load_sound',
                icon='FILEBROWSER',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.default_value, Sound):
            return f'bpy.data.sounds.get("{self.default_value.name}")'
