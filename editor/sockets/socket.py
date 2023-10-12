from ...utilities import warn
from ...utilities import Color
from ...utilities import WARNING_MESSAGES
from bpy.props import FloatVectorProperty
from bpy.props import StringProperty
from bpy.types import NodeLink
from bpy.types import NodeSocket
from bpy.types import NodeSocketInterface
from bpy.types import NodeSocketVirtual
import bpy


CONDITION_SOCKET_COLOR = Color.RGBA(0.8, 0.2, 0.2, 1.0)
PARAMETER_SOCKET_COLOR = Color.RGBA(.631, .631, .631, 1.0)
PARAM_BOOL_SOCKET_COLOR = Color.RGBA(.8, 0.651, .839, 1.0)
PARAM_INT_SOCKET_COLOR = Color.RGBA(.349, 0.549, .361, 1.0)
PARAM_COLOR_SOCKET_COLOR = Color.RGBA(.78, .78, .161, 1.0)
PARAM_LIST_SOCKET_COLOR = Color.RGBA(0.74, .65, .48, 1.0)
PARAM_DICT_SOCKET_COLOR = Color.RGBA(0.58, 0.48, .74, 1.0)
PARAM_OBJ_SOCKET_COLOR = Color.RGBA(0.929, 0.620, .361, 1.0)
PARAM_MAT_SOCKET_COLOR = Color.RGBA(.922, .459, .51, 1.0)
PARAM_GEOMTREE_SOCKET_COLOR = Color.RGBA(.45, .8, .58, 1.0)
PARAM_TEXT_SOCKET_COLOR = Color.RGBA(.388, .220, .388, 1.0)
PARAM_MESH_SOCKET_COLOR = Color.RGBA(.0, .839, .639, 1.0)
PARAM_COLL_SOCKET_COLOR = Color.RGBA(0.961, 0.961, .961, 1.0)
PARAM_SCENE_SOCKET_COLOR = Color.RGBA(0.5, 0.5, 0.6, 1.0)
PARAM_VECTOR_SOCKET_COLOR = Color.RGBA(0.388, 0.388, 0.78, 1.0)
PARAM_SOUND_SOCKET_COLOR = Color.RGBA(.388, .220, .388, 1.0)
PARAM_IMAGE_SOCKET_COLOR = Color.RGBA(.388, .220, .388, 1.0)
PARAM_LOGIC_BRICK_SOCKET_COLOR = Color.RGBA(0.9, 0.9, 0.4, 1.0)
PARAM_PYTHON_SOCKET_COLOR = Color.RGBA(0.2, 0.7, 1, 1.0)
ACTION_SOCKET_COLOR = Color.RGBA(0.2, .7, .7, 1.0)

CONDITION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]

SOCKET_TYPE_GENERIC = 0
SOCKET_TYPE_CONDITION = 1
SOCKET_TYPE_NUMERIC = 2
SOCKET_TYPE_INT = 3
SOCKET_TYPE_INT_POSITIVE = 4
SOCKET_TYPE_FLOAT = 5
SOCKET_TYPE_FLOAT_POSITIVE = 6
SOCKET_TYPE_STRING = 7
SOCKET_TYPE_BOOL = 8
SOCKET_TYPE_VECTOR = 9
SOCKET_TYPE_MATRIX = 10
SOCKET_TYPE_COLOR = 11
SOCKET_TYPE_OBJECT = 12
SOCKET_TYPE_DATA = 13
SOCKET_TYPE_DATABLOCK = 14
SOCKET_TYPE_UI = 15
SOCKET_TYPE_COLLECTION = 16
SOCKET_TYPE_VALUE = 17
SOCKET_TYPE_TEXT = 17
SOCKET_TYPE_SOUND = 17
SOCKET_TYPE_IMAGE = 17
SOCKET_TYPE_FONT = 17
SOCKET_TYPE_LIST = 17
SOCKET_TYPE_DICTIONARY = 17


BL_SOCKET_TYPES = [
    'VALUE',  # 0
    'MATERIAL',  # 1
    'VALUE',  # 2
    'INT',  # 3
    'INT',  # 4
    'VALUE',  # 5
    'VALUE',  # 6
    'STRING',  # 7
    'BOOLEAN',  # 8
    'VECTOR',  # 9
    'VECTOR',  # 10
    'RGBA',  # 11
    'OBJECT',  # 12
    'INT',  # 13
    'TEXTURE',  # 14
    'GEOMETRY',  # 15
    'COLLECTION',  # 16
    'VALUE'  # 17
]


_sockets = []


def socket_type(obj):

    class Interface(NodeSocketInterface):
        bl_socket_idname = obj.bl_idname
        nl_socket = obj
        hide_value = True
        type: StringProperty(default='VALUE')

        @classmethod
        def poll(self, context):
            return False

        def draw(self, context, layout):
            pass

        def draw_color(self, context):
            return self.nl_socket.color if self.nl_socket.color else PARAMETER_SOCKET_COLOR

    _sockets.append(obj)
    _sockets.append(Interface)
    return obj


def update_draw(self, context=None):
    tree = getattr(context.space_data, 'edit_tree')
    if tree:
        tree.changes_staged = True
    if hasattr(context, 'node'):
        context.node.update_draw(context)



class NodeSocketLogic:
    """Possible Types:
    - CUSTOM
    - VALUE
    - INT
    - BOOLEAN
    - VECTOR
    - ROTATION
    - STRING
    - RGBA
    - SHADER
    - OBJECT
    - IMAGE
    - GEOMETRY
    - COLLECTION
    - TEXTURE
    - MATERIAL
    """
    bl_idname = ''
    valid_sockets: list = []
    deprecated = False
    color = None
    nl_type = SOCKET_TYPE_VALUE
    type: StringProperty(default='VALUE')
    nl_color: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=4,
        default=PARAMETER_SOCKET_COLOR
    )

    def update_draw(self, context=None):
        pass

    @classmethod
    def get_id(cls):
        return cls.bl_idname

    def __init__(self):
        if self.color:
            self.nl_color = self.color
        self.type = BL_SOCKET_TYPES[self.nl_type]

    def check(self, tree):
        if self.deprecated:
            global WARNING_MESSAGES
            warn(f"Socket '{self.name if self.name else self.bl_label}' of node '{self.node.name}' in tree '{tree.name}' is deprecated and will be removed in a future version! Using default value for now, re-add node to avoid issues.")
            WARNING_MESSAGES.append(f"Deprecated Socket: '{self.node.name}': '{self.name if self.name else self.bl_label}' in '{tree.name}'. Delete and re-add node to avoid issues.")
            if not self.node.deprecated:
                self.node.use_custom_color = True
                self.node.color = (.8, .6, 0)

    def draw_color(self, context, node):
        return self.nl_color

    def on_validate(self, link, nodetree):
        """Called when an outgoing link is validated by `to_socket`"""
        pass

    def validate(self, link: NodeLink, from_socket: NodeSocket, nodetree):
        # while isinstance(from_socket.node, NodeReroute):
        #     links = from_socket.node.inputs[0].links
        #     if len(links) > 0:
        #         from_socket = links[0].from_socket
        #     else:
        #         link.is_valid = False
        #         return
        if not hasattr(from_socket, 'nl_type'):
            link.is_valid = True
            return
        if self.nl_type is SOCKET_TYPE_GENERIC:
            self.nl_color = from_socket.nl_color
            link.is_valid = True
            from_socket.on_validate(link, nodetree)
            return
        if from_socket.nl_type is SOCKET_TYPE_GENERIC:
            from_socket.nl_color = self.nl_color
            link.is_valid = True
            from_socket.on_validate(link, nodetree)
            return
        if len(self.valid_sockets) < 1:
            link.is_valid = True
            return
        link.is_valid = from_socket.nl_type in self.valid_sockets
        from_socket.on_validate(link, nodetree)

    def get_unlinked_value(self):
        raise NotImplementedError()


@socket_type
class NodeSocketLogicVirtual(NodeSocketVirtual, NodeSocketLogic):
    bl_idname = 'NodeSocketLogicVirtual'
    nl_type = SOCKET_TYPE_GENERIC
    color = (.188, .188, .188, 1)

    def draw(self, context, a, b, c):
        pass

    def on_validate(self, link, nodetree):
        nodetree.inputs.new(link.to_socket.bl_idname, link.to_socket.name)
        socket = self.node.outputs.new(link.to_socket.bl_idname, link.to_socket.name)
        self.node.outputs.new(self.bl_idname, '')
        nodetree.links.new(socket, link.to_socket)
        self.node.outputs.remove(self)
