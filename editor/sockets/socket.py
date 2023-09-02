from ...utilities import warn
from ...utilities import Color
from ...utilities import WARNING_MESSAGES


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


_sockets = []


def socket_type(obj):
    _sockets.append(obj)
    return obj


class NodeSocketLogic:
    bl_idname = ''
    valid_sockets: list = []
    deprecated = False
    nl_color: list = PARAMETER_SOCKET_COLOR

    @classmethod
    def get_id(cls):
        return cls.bl_idname

    def __init__(self):
        self.valid_sockets = []

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

    def validate(self, from_socket):
        pass

    def get_unlinked_value(self):
        raise NotImplementedError()
