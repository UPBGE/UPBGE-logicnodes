from ...utilities import Color


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


class NodeSocketLogic:
    valid_sockets: list = []
    nl_color: list = PARAMETER_SOCKET_COLOR

    def __init__(self):
        self.valid_sockets = []

    def draw_color(self, context, node):
        return self.nl_color

    def validate(self, from_socket):
        pass

    def get_unlinked_value(self):
        raise NotImplementedError()
