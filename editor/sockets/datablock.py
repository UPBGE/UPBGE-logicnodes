from .socket import SOCKET_COLOR_DATABLOCK, SOCKET_TYPE_DATABLOCK, SOCKET_TYPE_FONT, SOCKET_TYPE_IMAGE, SOCKET_TYPE_MATERIAL, SOCKET_TYPE_MESH, SOCKET_TYPE_SCENE, SOCKET_TYPE_SOUND, SOCKET_TYPE_TEXT, NodeSocketLogic
from .socket import socket_type
from bpy.types import NodeSocket

@socket_type
class NodeSocketLogicDatablock(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicDatablock"
    bl_label = "Datablock"

    default_value = None

    nl_color = SOCKET_COLOR_DATABLOCK
    nl_type = SOCKET_TYPE_DATABLOCK
    valid_sockets = [
        SOCKET_TYPE_DATABLOCK,
        SOCKET_TYPE_IMAGE,
        SOCKET_TYPE_MATERIAL,
        SOCKET_TYPE_SOUND,
        SOCKET_TYPE_FONT,
        SOCKET_TYPE_TEXT,
        SOCKET_TYPE_MESH,
        SOCKET_TYPE_SCENE
    ]

    def _draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return 'None'
