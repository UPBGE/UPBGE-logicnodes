from ...utilities import DEPRECATED, warn
from ...utilities import Color
from ...utilities import WARNING_MESSAGES
from bpy.props import BoolProperty
from bpy.props import StringProperty
from bpy.types import NodeLink
from bpy.types import NodeSocketVirtual
from bpy.types import NodeSocket
from bpy.types import NodeReroute
import bpy
if bpy.app.version[0] >= 4:
    from bpy.types import NodeTreeInterfaceSocket


SOCKET_COLOR_CONDITION = Color.RGBA(0.9, 0.3, 0.3, 1.0)
SOCKET_COLOR_GENERIC = Color.RGBA(.631, .631, .631, 1.0)
SOCKET_COLOR_BOOLEAN = Color.RGBA(.8, 0.651, .839, 1.0)
SOCKET_COLOR_INTEGER = Color.RGBA(.349, 0.549, .361, 1.0)
SOCKET_COLOR_COLOR = Color.RGBA(.78, .78, .161, 1.0)
SOCKET_COLOR_LIST = Color.RGBA(0.74, .65, .48, 1.0)
SOCKET_COLOR_DICTIONARY = Color.RGBA(0.58, 0.48, .74, 1.0)
SOCKET_COLOR_OBJECT = Color.RGBA(0.929, 0.620, .361, 1.0)
SOCKET_COLOR_MATERIAL = Color.RGBA(.922, .459, .51, 1.0)
SOCKET_COLOR_GEOTREE = Color.RGBA(.45, .8, .58, 1.0)
SOCKET_COLOR_TEXT = Color.RGBA(.388, .220, .388, 1.0)
SOCKET_COLOR_MESH = Color.RGBA(.0, .839, .639, 1.0)
SOCKET_COLOR_COLLECTION = Color.RGBA(0.961, 0.961, .961, 1.0)
SOCKET_COLOR_SCENE = Color.RGBA(0.5, 0.5, 0.6, 1.0)
SOCKET_COLOR_VECTOR = Color.RGBA(0.388, 0.388, 0.78, 1.0)
SOCKET_COLOR_ROTATION = Color.RGBA(0.651, 0.388, 0.78, 1.0)
SOCKET_COLOR_DATABLOCK = Color.RGBA(.388, .220, .388, 1.0)
SOCKET_COLOR_PYTHON = Color.RGBA(0.2, 0.7, 1, 1.0)
SOCKET_COLOR_STRING = Color.RGBA(0.439, .698, 1.0, 1.0)

CONDITION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]

SOCKET_TYPE_GENERIC = 0
SOCKET_TYPE_CONDITION = 1
# SOCKET_TYPE_NUMERIC = 2
SOCKET_TYPE_INT = 3
# SOCKET_TYPE_INT_POSITIVE = 4
SOCKET_TYPE_FLOAT = 5
# SOCKET_TYPE_FLOAT_POSITIVE = 6
SOCKET_TYPE_STRING = 7
SOCKET_TYPE_BOOL = 8
SOCKET_TYPE_VECTOR = 9
SOCKET_TYPE_MATRIX = 10
SOCKET_TYPE_COLOR = 11
SOCKET_TYPE_OBJECT = 12
# SOCKET_TYPE_DATA = 13
SOCKET_TYPE_DATABLOCK = 14
SOCKET_TYPE_UI = 15
SOCKET_TYPE_COLLECTION = 16
SOCKET_TYPE_VALUE = 17
SOCKET_TYPE_TEXT = 18
SOCKET_TYPE_SOUND = 19
SOCKET_TYPE_IMAGE = 20
SOCKET_TYPE_FONT = 21
SOCKET_TYPE_ACTION = 22
SOCKET_TYPE_ARMATURE = 23
SOCKET_TYPE_LIST = 24
SOCKET_TYPE_DICTIONARY = 25
SOCKET_TYPE_MATERIAL = 26
SOCKET_TYPE_NODETREE = 27
SOCKET_TYPE_MESH = 28
SOCKET_TYPE_PYTHON = 29
SOCKET_TYPE_SCENE = 30


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
    'STRING',  # 17
    'TEXTURE',  # 18
    'TEXTURE',  # 19
    'TEXTURE',  # 20
    'TEXTURE',  # 21
    'TEXTURE',  # 22
    'TEXTURE',  # 23
    'INT',  # 24
    'BOOLEAN',  # 25
    'TEXTURE',  # 26
    'TEXTURE',  # 27
    'GEOMETRY',  # 28
    'GEOMETRY',  # 29
    'MATERIAL'  # 30
]


_sockets = []


def socket_type(obj):

    _sockets.append(obj)
    
    if bpy.app.version[0] >= 4:
        class Interface(NodeTreeInterfaceSocket, obj):
            bl_socket_idname = obj.bl_idname
            nl_socket = obj
            hide_value = True
            type: StringProperty(default='VALUE')

            @classmethod
            def poll(self, context):
                return False

            def draw(self, context, layout):
                layout.prop(self, 'value')

            # def draw_color(self, context):
            #     return self.nl_socket.nl_color if self.nl_socket.nl_color else SOCKET_COLOR_GENERIC

        # _sockets.append(Interface)
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
    deprecated = False
    nl_color = SOCKET_COLOR_GENERIC
    nl_type = SOCKET_TYPE_VALUE
    nl_shape = 'CIRCLE'
    valid_sockets: list = None
    type: StringProperty(default='VALUE')
    identifier: StringProperty(default='')
    use_default_value: BoolProperty(default=False)
    skip_validation: BoolProperty()
    list_mode: BoolProperty()

    def update_draw(self, context=None):
        pass

    @property
    def linked_valid(self):
        return (
            self.is_linked and
            len(self.links) > 0 and
            self.links[0].from_socket.enabled and not
            self.links[0].from_node.mute
        )

    def is_valid_link(self, idx=0):
        return (
            self.is_linked and
            len(self.links) > 0 and
            self.links[idx].from_socket.enabled and not
            self.links[idx].from_node.mute
        )

    def _draw(self, context, layout, node, text):
        pass

    def draw(self, context, layout, node, text):
        if self.list_mode:
            layout.label(text=self.name)
        else:
            self._draw(context, layout, node, text)

    def get_from_socket(self):
        if self.is_multi_input or not len(self.links):
            return None
        from_socket = self.links[0].from_socket
        while isinstance(from_socket.node, NodeReroute):
            if not len(from_socket.links):
                return from_socket
            from_socket = from_socket.node.inputs[0].links[0].from_socket
        return from_socket

    @classmethod
    def get_id(cls):
        return cls.bl_idname

    def __init__(self):
        self.type = BL_SOCKET_TYPES[self.nl_type]
        if not self.use_default_value:
            self._update_prop_name()
            self.use_default_value = True

    def _update_prop_name(self):
        value = getattr(self, 'value', DEPRECATED)
        if value is not DEPRECATED:
            self.default_value = value
            # bpy.props.RemoveProperty(cls=self.__class__, attr='value')

    def check(self, tree):
        if self.deprecated:
            global WARNING_MESSAGES
            warn(f"Socket '{self.name if self.name else self.bl_label}' of node '{self.node.name}' in tree '{tree.name}' is deprecated and will be removed in a future version! Using default value for now, re-add node to avoid issues.")
            WARNING_MESSAGES.append(f"Deprecated Socket: '{self.node.name}': '{self.name if self.name else self.bl_label}' in '{tree.name}'. Delete and re-add node to avoid issues.")
            if not self.node.deprecated:
                self.node.use_custom_color = True
                self.node.color = (.8, .6, 0)

    @classmethod
    def draw_color_simple(cls):
        return cls.nl_color

    def draw_color(self, context, layout):
        return self.__class__.nl_color

    @classmethod
    def draw_interface(cls, context, layout):
        pass

    def on_validate(self, link, nodetree):
        """Called when an outgoing link is validated by `to_socket`"""
        pass

    def validate(self, link: NodeLink, from_socket: NodeSocket, nodetree):
        while isinstance(from_socket.node, NodeReroute) and len(from_socket.node.inputs[0].links) > 0:
            from_socket = from_socket.node.inputs[0].links[0].from_socket
        if not hasattr(from_socket, 'nl_type'):
            link.is_valid = True
            return
        if self.nl_type is SOCKET_TYPE_VALUE:
            link.is_valid = True
            return
        if self.nl_type is SOCKET_TYPE_GENERIC:
            # self.__class__.nl_color = from_socket.nl_color
            link.is_valid = True
            from_socket.on_validate(link, nodetree)
            return
        if from_socket.nl_type is SOCKET_TYPE_GENERIC:
            # from_socket.__class__.nl_color = self.nl_color
            link.is_valid = True
            from_socket.on_validate(link, nodetree)
            return
        if self.valid_sockets is None:
            link.is_valid = from_socket.nl_type is self.nl_type
            return
        if len(self.valid_sockets) < 1:
            link.is_valid = True
            return
        link.is_valid = from_socket.nl_type in self.valid_sockets
        from_socket.on_validate(link, nodetree)

    def get_default_value(self):
        return f'[{self.get_unlinked_value()}]' if self.list_mode else self.get_unlinked_value()

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
