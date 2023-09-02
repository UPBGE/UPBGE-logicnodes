import math
import bpy
import bge_netlogic
from bge_netlogic import utilities as utils
from  bge_netlogic.utilities import ERROR_MESSAGES, WARNING_MESSAGES
from ui import LogicNodeTree
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
import socket  # used for automatically setting IP address for server node

INVALID = 'INVALID'

CONDITION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]


_nodes = []


_enum_look_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]")
]

_enum_vector_types = [
    ("0", "Vector", "Vector XYZ"),
    ("1", "Euler", "Euler XYZ")
]

_enum_local_oriented_axis = [
    ("0", "+X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "+Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "+Z Axis", "The Local Z Axis [Integer Value 2]"),
    ("3", "-X Axis", "The Local X Axis [Integer Value 3]"),
    ("4", "-Y Axis", "The Local Y Axis [Integer Value 4]"),
    ("5", "-Z Axis", "The Local Z Axis [Integer Value 5]")
]

_enum_mouse_wheel_direction = [
    ("1", "Scroll Up", "Mouse Wheel Scrolled Up [1]"),
    ("2", "Scroll Down", "Mouse Wheel Scrolled Down [2]"),
    ("3", "Scroll Up or Down", "Mouse Wheel Scrolled either Up or Down[3]")
]


_enum_vector_math_options = [
    ("scale", "Scale", "A multiplied by Scale"),
    ("length", "Length", "Length of A"),
    ("distance", "Distance", "Distance between A and B"),
    None,
    ("dot", "Dot Product", "A dot B"),
    ("faceforward", "Faceforward", "Orients a vector A to point away from a surface B as defined by its normal C. Returns A if A.dot(B) < 0 else -A"),
    ("refract", "Refract", "For a given incident vector A, a surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R"),
    ("reflect", "Reflect", "Reflect A around the normal B. B doesn't need to be normalized"),
    ("project", "Project", "Project this vector onto another"),
    ("cross", "Cross Product", "Project A onto B"),
    None,
    ("multadd", "Multiply Add", "A * B + C"),
    ("divide", "Divide", "Entry-wise divide"),
    ("multiply", "Multiply", "Entry-wise multiply"),
    ("subtract", "Subtract", "A - B"),
    ("add", "Add", "A + B"),
    ("", "Operation", ""),
    None,
    ("normalize", "Normalize", "Rescale all values to 0 - 1"),
    ("lerp", "Lerp", "Linear Interpolation between the two vectors"),
    ("slerp", "Spherical Lerp", "Spherical Interpolation between the two vectors"),
    ("negate", "Negate", "Multiply all values by -1")
]


_enum_type_casts = [
    ("int", "To Integer", "Convert this value to an integer type"),
    ("bool", "To Boolean", "Convert this value to a boolean type"),
    ("str", "To String", "Convert this value to a string type"),
    ("float", "To Float", "Convert this value to a float type")
]


_enum_object_property_types = [
    ('GAME', 'Game Property', 'Edit Game Property'),
    ('ATTR', 'Attribute', 'Edit Internal Attribute (can be used in materials)')
]


_enum_2d_filters = [
    ('FXAA', 'FXAA', 'Fast Anti-Aliasing'),
    ('HBAO', 'HBAO', 'Horizon-Based Ambient Occlusion'),
    ('SSAO', 'SSAO', 'Screen-Space Ambient Occlusion'),
    ('VIGNETTE', 'Vignette', 'Fade to color at screen edges'),
    ('BRIGHTNESS', 'Brightness', 'Overall brightness'),
    ('CHROMAB', 'Chromatic Aberration', 'Lens light bending effect'),
    ('GRAYSCALE', 'Grayscale', 'Convert image to grayscale'),
    ('LEVELS', 'Levels', 'Control color levels'),
    ('MIST', 'Mist', 'Classic depth fog implementation')
]


_enum_constraint_types = [
    (
        "bge.constraints.POINTTOPOINT_CONSTRAINT",
        "Ball",
        "Allow rotation around all axis"
    ),
    (
        "bge.constraints.LINEHINGE_CONSTRAINT",
        "Hinge",
        "Work on one plane, allow rotations on one axis only"
    ),
    (
        "bge.constraints.CONETWIST_CONSTRAINT",
        "Cone Twist",
        (
            'Allow rotations around all axis with limits for the cone '
            'and twist axis'
        )
    ),
    (
        "bge.constraints.GENERIC_6DOF_CONSTRAINT",
        "Generic 6 DOF",
        "No constraints by default, limits can be set individually"
    )
]

_enum_vehicle_axis = [
    ("REAR", "Rear", "Apply to wheels without steering"),
    ("FRONT", "Front", "Apply to wheels with steering"),
    ("ALL", "All", "Apply to all wheels")
]


_enum_readable_member_names = [
    ("worldPosition", "Position (Global)", "The World Position of the object"),
    ("localPosition", "Position (Local)", "The local position of the object"),
    (
        "worldOrientation",
        "Rotation (Global)",
        "The World Orientation of the object"
    ), (
        "localOrientation",
        "Rotation (Local)",
        "The local orientation of the object"
    ), (
        "worldLinearVelocity",
        "Linear Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Linear Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Angular Velocity (Global)",
        "The local angular velocity of the object"
    ), (
        "localAngularVelocity",
        "Angular Velocity (Local)",
        "The local angular velocity of the object"
    ), (
        "worldTransform",
        "Transform (Global)",
        (
            'The World Transform of the '
            'object'
        )
    ), (
        "localTransform",
        "Transform (Local)",
        (
            'The local transform of the '
            'object'
        )
    ),
    ("worldScale", "World Scale", "The global scale of the object"),
    ("localScale", "Local Scale", "The local scale of the object"),
    ("name", "Name", "The name of the object"),
    ("color", "Color", "The solid color of the object"),
    (
        "visible",
        "Visibility",
        "True if the object is set to visible, False if it is set of invisible"
    )
]

_enum_writable_member_names = [
    ("color", "Color", "The solid color of the object"),
    ("worldPosition", "Position (Global)", "The World Position of the object"),
    ("localPosition", "Position (Local)", "The local position of the object"),
    (
        "worldOrientation",
        "Rotation (Global)",
        "The World Orientation of the object"
    ), (
        "localOrientation",
        "Rotation (Local)",
        "The local orientation of the object"
    ), (
        "worldLinearVelocity",
        "Linear Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Linear Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Angular Velocity (Global)",
        "The local rotational velocity of the object"
    ), (
        "localAngularVelocity",
        "Angular Velocity (Local)",
        "The local rotational velocity of the object"
    ), (
        "worldTransform",
        "Transform (Global)",
        (
            'The World Transform of the '
            'object'
        )
    ), (
        "localTransform",
        "Transform (Local)",
        (
            'The local transform of the '
            'object'
        )
    ),
    ("worldScale", "Scale", "The global scale of the object")
]

_enum_vsync_modes = [
    ("bge.render.VSYNC_OFF", "Off", "Disable Vsync"),
    ("bge.render.VSYNC_ON", "On", "Enable Vsync"),
    (
        "bge.render.VSYNC_ADAPTIVE",
        "Adaptive",
        (
            'Enable adaptive Vsync '
            '(if supported)'
        )
    )
]

_enum_string_ops = [
    ("0", "Postfix", "Insert A after String"),
    ("1", "Prefix", "Insert A before String"),
    ("2", "Infix", "Insert A before String, B after String."),
    ("3", "Remove Last", "Remove Last Character from String"),
    ("4", "Remove First", "Remove First Character from String"),
    (
        "5",
        "Replace",
        'Replace all occurences of A with B'
    ),
    ("6", "Upper Case", "Convert to Upper Case"),
    ("7", "Lower Case", "Convert to Lower Case"),
    (
        "8",
        "Remove Range",
        'Remove characters from index A to index B'
    ),
    (
        "9",
        "Insert At",
        "Insert A at index B"
    ),
    (
        "10",
        "Length",
        "Character Count (returns a Number)"
    ),
    (
        "11",
        "Substring",
        "Characters between index A and index B"
    ),
    (
        "12",
        "First Index Of",
        "Position of the first occurence of A"
    ),
    (
        "13",
        "Last Index Of",
        "Position of the last occurence of A"
    )
]

_enum_math_operations = [
    ("ADD", "Add", "Sum A and B"),
    ("SUB", "Subtract", "Subtract B from A"),
    ("DIV", "Divide", "Divide A by B"),
    ("MUL", "Multiply", "Multiply A by B"),
    ("POW", "Power", "A to the power of B"),
    ("MOD", "Modulo", "Modulo of A by B"),
    ("FDIV", "Floor Divide", "Floor Divide A by B"),
    ("MATMUL", "Matrix Multiply", "Transform A by B")
]

_enum_greater_less = [
    ("GREATER", "Greater", "Value greater than Threshold"),
    ("LESS", "Less", "Value less than Threshold")
]

_enum_in_or_out = [
    ("INSIDE", "Within", "Value is within Range"),
    ("OUTSIDE", "Outside", "Value is outside Range")
]

_enum_logic_operators = [
    ("0", "Equal", "A equals B"),
    ("1", "Not Equal", "A not equals B"),
    ("2", "Greater Than", "A greater than B"),
    ("3", "Less Than", "A less than B"),
    ("4", "Greater or Equal", "A greater or equal to B"),
    ("5", "Less or Equal", "A less or equal to B")
]


_enum_controller_stick_operators = [
    ("0", "Left Stick", "Left Stick Values"),
    ("1", "Right Stick", "Right Stick Values")
]

_enum_controller_trigger_operators = [
    ("0", "Left Trigger", "Left Trigger Values"),
    ("1", "Right Trigger", "Right Trigger Values")
]

_enum_vrcontroller_trigger_operators = [
    ("0", "Left", "Left Controller Values"),
    ("1", "Right", "Right Controller Values")
]


_enum_controller_buttons_operators = [
    ("0", "A / Cross", "A / Cross Button"),
    ("1", "B / Circle", "B / Circle Button"),
    ("2", "X / Square", "X / Square Button"),
    ("3", "Y / Triangle", "Y / Triangle Button"),
    ("4", "Select / Share", "Select / Share Button"),
    ("6", "Start / Options", "Start / Options Button"),
    ("7", "L3", "Left Stick Button"),
    ("8", "R3", "Right Stick Button"),
    ("9", "LB / L1", "Left Bumper / L1 Button"),
    ("10", "RB / R1", "Right Bumper / R1 Button"),
    ("11", "D-Pad Up", "D-Pad Up Button"),
    ("12", "D-Pad Down", "D-Pad Down Button"),
    ("13", "D-Pad Left", "D-Pad Left Button"),
    ("14", "D-Pad Right", "D-Pad Right Button")
]


_enum_play_mode_values = [
    ("bge.logic.KX_ACTION_MODE_PLAY", "Play", "Play the action once"),
    ("bge.logic.KX_ACTION_MODE_LOOP", "Loop", "Loop the action"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG",
        "Ping Pong",
        "Play the action in one direction then in the opposite one"
    ),
    ("bge.logic.KX_ACTION_MODE_PLAY + 3", "Play Stop", "Play the action once"),
    ("bge.logic.KX_ACTION_MODE_LOOP + 3", "Loop Stop", "Loop the action"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG + 3",
        "Ping Pong Stop",
        "Play the action in one direction then in the opposite one"
    )
]

_enum_spawn_types = [
    ("Simple", "Simple", "Spawn an instance without behavior"),
    ("SimpleBullet", "Simple Bullet", "Spawn a bullet that travels linearly along its local +Y axis"),
    ("PhysicsBullet", "Physical Bullet", "Spawn a bullet that travels along a trajectory aimed at its local +Y axis")
]

_serialize_types = [
    ("builtin", "Built-In", "Serialize Built-In data type (int, float, bool, dict, etc.)"),
    ("Vec2", "2D Vector", "Serialize a 2D Vector"),
    ("Vec3", "3D Vector", "Serialize a 3D Vector"),
    ("Vec4", "4D Vector", "Serialize a 4D Vector"),
    ("Mat3", "3x3 Matrix", "Serialize a 3x3 Matrix"),
    ("Mat4", "4x4 Matrix", "Serialize a 4x4 Matrix"),
    ("GameObj", "Game Object", "Serialize a Game Object (Note: Not all data can be serialized)")
]


_enum_msg_types = [
    ("INFO", "Info", "Will print the message in white (on-screen console)"),
    ("DEBUG", "Debug", "Will print the message in light yellow (on-screen console)"),
    ("WARNING", "Warning", "Will print the message in yellow (on-screen console)"),
    ("ERROR", "Error", "Will print the message in red (on-screen console)"),
    ("SUCCESS", "Success", "Will print the message in green (on-screen console)")
]





def filter_materials(self, item):
    if item.is_grease_pencil:
        return False
    return True


def filter_geometry_nodes(self, item):
    if isinstance(item, bpy.types.GeometryNodeTree):
        return True
    return False


def filter_lights(self, item):
    if (
        isinstance(item.data, bpy.types.AreaLight)
        or isinstance(item.data, bpy.types.PointLight)
        or isinstance(item.data, bpy.types.SpotLight)
        or isinstance(item.data, bpy.types.SunLight)
    ):
        return True
    return False


def filter_texts(self, item):
    if (
        item.name.startswith('nl_')
    ):
        return False
    return True


def filter_navmesh(self, item):
    if item.game.physics_type == 'NAVMESH':
        return True
    return False


def filter_camera(self, item):
    if isinstance(item.data, bpy.types.Camera):
        return True
    return False


def filter_speaker(self, item):
    if isinstance(item.data, bpy.types.Speaker):
        return True
    return False


def filter_armatures(self, item):
    if (
        isinstance(item.data, bpy.types.Armature)
    ):
        return True
    return False


def filter_curves(self, item):
    if (
        isinstance(item.data, bpy.types.Curve)
    ):
        return True
    return False


def filter_logic_trees(self, item):
    if (
        isinstance(item, bge_netlogic.ui.LogicNodeTree)
    ):
        return True
    return False


def filter_node_groups(self, item):
    if (
        isinstance(item, bpy.types.ShaderNodeTree)
    ):
        return True
    return False


def parse_field_value(value_type, value):
    t = value_type
    v = value

    if t == "NONE":
        return "None"

    if t == "INTEGER":
        try:
            return int(v)
        except ValueError:
            return "0.0"

    if t == "FLOAT":
        try:
            return float(v)
        except ValueError:
            return "0.0"

    if t == "STRING":
        return '"{}"'.format(v)

    if t == "FILE_PATH":
        return '"{}"'.format(v)

    if t == "BOOLEAN":
        return v

    raise ValueError(
        "Cannot parse enum {} type for NLValueFieldSocket".format(t)
    )


def update_tree_code(self, context):
    pass
    # utils.set_compile_status(utils.TREE_MODIFIED)
    # if utils.is_compile_status(utils.TREE_COMPILED_ALL):
    #     return
    # if not hasattr(context.space_data, 'edit_tree'):
    #     return
    # tree = context.space_data.edit_tree
    # if not tree:
    #     return
    # for node in tree.nodes:
    #     if isinstance(node, NLNode):
    #         try:
    #             node.update_draw()
    #         except Exception:
    #             pass
    # if not getattr(bpy.context.scene.logic_node_settings, 'auto_compile'):
    #     return
    # bge_netlogic.update_current_tree_code()


def update_draw(self, context):
    if not hasattr(context.space_data, 'edit_tree'):
        return
    tree = context.space_data.edit_tree
    for node in tree.nodes:
        if isinstance(node, NLNode):
            try:
                node.update_draw()
            except Exception as e:
                utils.error(f'Failed node {node}, {e}')
                pass


def socket_field(s):
    return parse_field_value(s.value_type, s.value)


def keyboard_key_string_to_bge_key(ks):
    ks = ks.replace("ASTERIX", "ASTER")

    if ks == "NONE":
        return "None"

    if ks == "RET":
        ks = "ENTER"

    if ks.startswith("NUMPAD_"):
        ks = ks.replace("NUMPAD_", "PAD")
        if("SLASH" in ks or "ASTER" in ks or "PLUS" in ks):
            ks = ks.replace("SLASH", "SLASHKEY")
            ks = ks.replace("ASTER", "ASTERKEY")
            ks = ks.replace("PLUS", "PLUSKEY")
        return "bge.events.{}".format(ks)

    x = "{}KEY".format(ks.replace("_", ""))

    return "bge.events.{}".format(x)


class NetLogicType:
    pass


class NLSocket:
    valid_sockets: list = []
    nl_color: list = utils.Color.RGBA(.631, .631, .631, 1.0)
    type: StringProperty(default='VALUE')
    shape: StringProperty(default='')

    def __init__(self):
        self.socket_id = INVALID
        self.valid_sockets = []
        # self.display_shape = 'CIRCLE'
    #     if len(self.shape):
    #         self.shape_setup()

    # def shape_setup(self):
    #     pass

    def draw_color(self, context, node):
        return self.nl_color

    def validate(self, link, from_socket):
        link.is_valid = False
        pass

    def get_unlinked_value(self):
        raise NotImplementedError()


class NLNode(NetLogicType):
    nl_module = None

    def write_cell_declaration(self, cell_varname, line_writer):
        classname = self.get_netlogic_class_name()
        line_writer.write_line("{} = {}()", cell_varname, classname)

    @property
    def tree(self):
        for tree in bpy.data.node_groups:
            if not isinstance(tree, LogicNodeTree):
                continue
            nodes = [node for node in tree.nodes]
            if self in nodes:
                return tree

    def setup(
        self,
        cell_varname,
        uids
    ):
        text = ''
        global ERROR_MESSAGES
        for t in self.get_attributes():
            field_name = t[0]
            field_value = t[1]
            if callable(field_value):
                field_value = field_value()
            text += f'        {cell_varname}.{field_name} = {field_value}\n'
        for socket in self.inputs:
            try:
                text += self.write_socket_field_initialization(
                    socket,
                    cell_varname,
                    uids
                )
                # self.mute = False
            except IndexError as e:
                utils.error(
                    f"Index error for node '{self.name}'. This normally happens when a node has sockets added or removed in an update. Try re-adding the node to resolve this issue."
                )
                # self.mute = True
                ERROR_MESSAGES.append(f'{self.name}: Index Error. FIX: Delete and re-add node; issue might be a linked input node as well.')
                self.use_custom_color = True
                self.color = (1, 0, 0)
            except Exception as e:
                utils.error(
                    f'Error occured when writing sockets for {self.__class__} Node: {e}\n'
                    f'\tInfo:\n'
                    f'\tSocket: {socket}\n'
                    f'\tCellname: {cell_varname}\n'
                    f'\tNode: {self.label if self.label else self.name}\n'
                    '---END ERROR'
                )
                # self.mute = True
                ERROR_MESSAGES.append(f'{self.name}: Unknown Error: {e}')
                self.use_custom_color = True
                self.color = (1, 0, 0)
        return text

    def write_socket_field_initialization(
        self,
        socket,
        cell_varname,
        uids
    ):
        text = ''
        input_names = self.get_input_names()
        input_socket_index = self._index_of(socket, self.inputs)
        field_name = None
        if input_names:
            field_name = input_names[input_socket_index]
        else:
            field_name = self.get_field_name_for_socket(socket)
        field_value = None
        if socket.is_linked:
            field_value = self.get_linked_socket_field_value(
                socket,
                cell_varname,
                field_name,
                uids
            )
        else:
            field_value = socket.get_unlinked_value()
        # line_writer.write_line(
        #     "\t{}.{} = {}",
        #     cell_varname,
        #     field_name,
        #     field_value
        # )
        text += f'        {cell_varname}.{field_name} = {field_value}\n'
        return text

    def get_attributes(self):
        """
        Return a list of (field_name, field_value) tuples, where field_name
        couples to output socket with a cell field and field_value is
        either a value or a no-arg callable producing value
        :return: the non socket fields initializers
        """
        return []

    def get_import_module(self):
        return self.nl_module

    def get_input_names(self):
        return None

    def get_field_name_for_socket(self, socket):
        utils.debug("not implemented in ", self)
        raise NotImplementedError()

    def get_netlogic_class_name(self):
        raise NotImplementedError()

    def _index_of(self, item, a_iterable):
        i = 0
        for e in a_iterable:
            if e == item:
                return i
            i += 1

    def get_linked_socket_field_value(
        self,
        socket,
        cell_varname,
        field_name,
        uids
    ):
        output_node = socket.links[0].from_socket.node
        output_socket = socket.links[0].from_socket

        while isinstance(output_node, bpy.types.NodeReroute):
            # cycle through and reset output_node until master is met
            if not output_node.inputs[0].links:
                return None
            next_socket = output_node.inputs[0].links[0].from_socket
            next_node = next_socket.node
            output_socket = next_socket
            if isinstance(next_node, NLNode):
                break
            output_node = next_node

        if isinstance(output_node, bpy.types.NodeReroute):
            output_node = output_node.inputs[0].links[0].from_socket.node
        output_socket_index = self._index_of(
            output_socket,
            output_node.outputs
        )

        if not hasattr(output_node, 'nl_module'):
            raise Exception('No NLNode')
        output_node_varname = uids.get_varname_for_node(output_node)
        output_map = output_node.get_output_names()

        if output_map:
            varname = output_map[output_socket_index]
            if varname is utils.OUTCELL:
                return output_node_varname
            else:
                return '{}.{}'.format(output_node_varname, varname)
        else:
            return output_node_varname

    def get_output_names(self):
        return None

    def update(self):
        # bge_netlogic.update_current_tree_code()
        pass


class NLConditionSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLConditionSocket"


class NodeSocketPseudoCondition(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPseudoConditionSocket"


class NLParameterSocket(bpy.types.NodeSocket):
    bl_idname = 'NLParameterSocket'


class NLDictSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLDictSocket"


class NLUISocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLUISocket"


class NLListSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLListSocket"


class NLListItemSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLListItemSocket"


class NLCollisionMaskSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCollisionMaskSocket"


class NLLogicBrickSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLLogicBrickSocket"


class NLPythonSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPythonSocket"


class NLAbstractNode(NLNode):
    bl_icon = 'DOT'
    nl_separate = False
    deprecated = False
    search_tags = []

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

    def insert_link(self, link):
        to_socket = link.to_socket
        from_socket = link.from_socket
        # try:
        #     to_socket.validate(link, from_socket)
        # except Exception as e:
        #     utils.warning(e)
        #     utils.debug(
        #         'Receiving Node not a Logic Node Type, skipping validation.'
        #     )

    def add_input(self, cls, name, settings={}):
        ipt = self.inputs.new(cls.bl_idname, name)
        for key, val in settings.items():
            setattr(ipt, key, val)

    def add_output(self, cls, name, settings={}):
        ipt = self.outputs.new(cls.bl_idname, name)
        for key, val in settings.items():
            setattr(ipt, key, val)

    def free(self):
        pass

    def check(self, tree):
        if self.deprecated:
            global WARNING_MESSAGES
            utils.deprecate(self, tree)
            WARNING_MESSAGES.append(f"Deprecated Node: '{self.name}' in '{tree.name}'. Delete to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)
        for socket in self.inputs:
            socket.check(tree)
        for socket in self.outputs:
            socket.check(tree)

    def draw_buttons(self, context, layout):
        pass

    def update_draw(self):
        pass

    def update(self):
        update_tree_code(self, bpy.context)


###############################################################################
# Basic Nodes
###############################################################################


class NLConditionNode(bpy.types.Node, NLAbstractNode):
    nl_nodetype = 'CON'

    def init(self, context):
        self.use_custom_color = (
            bpy
            .context
            .scene
            .logic_node_settings
            .use_custom_node_color
        )
        self.color = CONDITION_NODE_COLOR


class NLActionNode(bpy.types.Node, NLAbstractNode):
    nl_nodetype = 'ACT'

    def init(self, context):
        self.use_custom_color = (
            bpy
            .context
            .scene
            .logic_node_settings
            .use_custom_node_color
        )
        self.color = ACTION_NODE_COLOR


class NLParameterNode(bpy.types.Node, NLAbstractNode):
    nl_nodetype = 'PAR'

    def init(self, context):
        self.use_custom_color = (
            bpy
            .context
            .scene
            .logic_node_settings
            .use_custom_node_color
        )
        self.color = PARAMETER_NODE_COLOR
        self.master_nodes = []


###############################################################################
# Pointer Sockets
###############################################################################


class NLGameObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGameObjectSocket"


class NLCameraSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCameraSocket"


class NLSpeakerSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSpeakerSocket"


class NLNavMeshSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNavMeshSocket"


class NLLightObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLLightObjectSocket"


class NLArmatureObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLArmatureObjectSocket"


class NLCurveObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCurveObjectSocket"


class NLGamePropertySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGamePropertySocket"


class NLArmatureBoneSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLArmatureBoneSocket"


class NLBoneConstraintSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBoneConstraintSocket"


class NLGeomNodeTreeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGeomNodeTreeSocket"


class NLNodeGroupSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNodeGroupSocket"


class NLNodeGroupNodeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNodeGroupNodeSocket"


class NLMaterialSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMaterialSocket"


class NLTreeNodeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTreeNodeSocket"


class NLSceneSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSceneSocket"


class NLTextIDSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTextIDSocket"


class NLMeshSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMeshSocket"


class NLGameObjectNameSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGameObjectNameSocket"


class NLCollectionSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCollectionSocket"


class NLSocketLogicTree(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLogicTree"


class NodeSocketLogicAnimation(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLAnimationSocket"


class NLSoundFileSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSoundFileSocket"


class NLImageSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLImageSocket"


class NLFontSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFontSocket"


###############################################################################
# String Pointer Sockets
###############################################################################


class NLGlobalCatSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGlobalCatSocket"


class NLGlobalPropSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGlobalPropSocket"


###############################################################################
# Value Sockets
###############################################################################


class NLSocketAlphaFloat(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketAlphaFloat"


class NLSocketLoopCount(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLoopCount"


class NLBooleanSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBooleanSocket"


class NLXYZSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLXYZSocket"


class NLInvertedXYSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLInvertedXYSocket"


class NLPositiveFloatSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveFloatSocket"


class NLQuotedStringFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLQuotedStringFieldSocket"


class NLFilePathSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFilePathSocket"


class NLIntegerFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLIntegerFieldSocket"


class NLPositiveIntegerFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveIntegerFieldSocket"


class NLPositiveIntCentSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveIntCentSocket"


class NLValueFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLValueFieldSocket"


class NLOptionalValueFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLOptionalValueFieldSocket"


class NLKeyboardKeySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLKeyboardKeySocket"


class NLMouseButtonSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMouseButtonSocket"


class NLPlayActionModeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPlayActionModeSocket"


class NLFloatFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFloatFieldSocket"


class NLFloatAngleSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFloatAngleSocket"


class NLTimeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTimeSocket"


class NLVec2FieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVec2FieldSocket"


class NLAngleLimitSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLAngleLimitSocket"


class NLVec3FieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVec3FieldSocket"


class NLVec3RotationSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVec3RotationSocket"


class NLVelocitySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVelocitySocket"


class NLColorSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLColorSocket"


class NLColorAlphaSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLColorAlphaSocket"


class NLVectorSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVectorSocket"


class NLSocketLocalAxis(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLocalAxis"


class NLSocketOrientedLocalAxis(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketOrientedLocalAxis"


class NLBlendActionModeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBlendActionMode"


###############################################################################
# NODES
###############################################################################


# Parameters


class NLDrawLine(NLActionNode):
    bl_idname = "NLDrawLine"
    bl_label = "Line"
    nl_category = 'Render'
    nl_subcat = 'Draw'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, 'Condition')
        self.add_input(NLColorSocket, 'Color')
        self.add_input(NLVec3FieldSocket, 'From')
        self.add_input(NLVec3FieldSocket, 'To')
        self.add_output(NLConditionSocket, "Done")

    def get_input_names(self):
        return ['condition', 'color', 'from_point', 'to_point']

    def get_netlogic_class_name(self):
        return "ULDrawLine"


_nodes.append(NLDrawLine)


class NLDrawCube(NLActionNode):
    bl_idname = "NLDrawCube"
    bl_label = "Cube"
    nl_category = 'Render'
    nl_subcat = 'Draw'
    nl_module = 'actions'

    use_volume_origin: BoolProperty(
        name='Use Volume Origin',
        description='Offset the origin by half of the cube width on each axis',
        default=False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "use_volume_origin")

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, 'Condition')
        self.add_input(NLColorSocket, 'Color')
        self.add_input(NLVec3FieldSocket, 'Origin')
        self.add_input(NLFloatFieldSocket, 'Width')
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, "Done")

    def get_attributes(self):
        return [("use_volume_origin", lambda: f'{self.use_volume_origin}')]

    def get_input_names(self):
        return ['condition', 'color', 'origin', 'width']

    def get_netlogic_class_name(self):
        return "ULDrawCube"


_nodes.append(NLDrawCube)


class NLDrawBox(NLActionNode):
    bl_idname = "NLDrawBox"
    bl_label = "Box"
    nl_category = 'Render'
    nl_subcat = 'Draw'
    nl_module = 'actions'

    use_volume_origin: BoolProperty(
        name='Use Volume Origin',
        description='Offset the origin by half of the box dimensions on each axis',
        default=False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "use_volume_origin")

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, 'Condition')
        self.add_input(NLColorSocket, 'Color')
        self.add_input(NLVec3FieldSocket, 'Origin')
        self.add_input(NLFloatFieldSocket, 'Width (X)')
        self.inputs[-1].value = 1.0
        self.add_input(NLFloatFieldSocket, 'Length (Y)')
        self.inputs[-1].value = 1.0
        self.add_input(NLFloatFieldSocket, 'Height (Z)')
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, "Done")

    def get_attributes(self):
        return [("use_volume_origin", lambda: f'{self.use_volume_origin}')]

    def get_input_names(self):
        return ['condition', 'color', 'origin', 'width', 'length', 'height']

    def get_netlogic_class_name(self):
        return "ULDrawBox"


_nodes.append(NLDrawBox)


class NLRunActuatorNode(NLActionNode):
    bl_idname = "NLRunActuatorNode"
    bl_label = "Run Actuator"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLLogicBrickSocket, "From Controller")
        self.inputs[-1].ref_index = 1
        self.add_input(NLLogicBrickSocket, "Actuator")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'actuators'
        self.add_output(NLConditionSocket, 'Done')

    def get_controller(self):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        obj_socket = self.inputs[1]
        cont_name = self.inputs[2].value
        if not cont_name:
            return False
        if not obj_socket.use_owner and obj_socket.value:
            if cont_name in obj_socket.value.game.controllers:
                cont = obj_socket.value.game.controllers[cont_name]
                return isinstance(cont, bpy.types.PythonController)
        else:
            for sc_ob in bpy.data.objects:
                if f'{utils.NLPREFIX}{tree.name}' in sc_ob.game.properties:
                    if cont_name in sc_ob.game.controllers:
                        cont = sc_ob.game.controllers[cont_name]
                        return isinstance(cont, bpy.types.PythonController)
        return False

    def draw_buttons(self, context, layout):
        if not self.get_controller():
            col = layout.column()
            col.label(text='Selected Brick', icon='ERROR')
            col.label(text='not a Python Controller!')

    def update_draw(self):
        self.inputs[3].enabled = self.get_controller()

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRunActuator"

    def get_input_names(self):
        return ["condition", 'game_obj', 'cont_name', 'act_name']


_nodes.append(NLRunActuatorNode)


class NLSetSensorValueNode(NLActionNode):
    bl_idname = "NLSetSensorValueNode"
    bl_label = "Set Sensor Value"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLLogicBrickSocket, "Sensor")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'sensors'
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, "")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetSensorValue"

    def get_input_names(self):
        return ["condition", 'game_obj', 'sens_name', 'field', 'value']


_nodes.append(NLSetSensorValueNode)


class NLSetActuatorValueNode(NLActionNode):
    bl_idname = "NLSetActuatorValueNode"
    bl_label = "Set Actuator Value"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLLogicBrickSocket, "Actuator")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'actuators'
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, "")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetActuatorValue"

    def get_input_names(self):
        return ["condition", 'game_obj', 'act_name', 'field', 'value']


_nodes.append(NLSetActuatorValueNode)


class NLVectorAngleCheck(NLParameterNode):
    bl_idname = "NLVectorAngleCheck"
    bl_label = "Check Angle"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'
    operator: EnumProperty(
        name='Operation',
        items=_enum_logic_operators,
        update=update_draw
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLVec3FieldSocket, "Vector 1")
        self.add_input(NLVec3FieldSocket, "Vector 2")
        self.add_input(NLFloatFieldSocket, "Value")
        self.add_output(NLConditionSocket, 'If True')
        self.add_output(NLFloatFieldSocket, "Angle")

    def get_netlogic_class_name(self):
        return "ULVectorAngleCheck"

    def get_input_names(self):
        return ["vector", 'vector_2', 'value']

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            'operator',
            text=''
        )

    def get_output_names(self):
        return ['OUT', 'ANGLE']

    def get_attributes(self):
        return [
            ("op", lambda: f'"{self.operator}"'),
        ]


_nodes.append(NLVectorAngleCheck)


class NLGetSensorNode(NLConditionNode):
    bl_idname = "NLGetSensorNode"
    bl_label = "Sensor Positive"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLLogicBrickSocket, 'Sensor')
        self.inputs[-1].brick_type = 'sensors'
        self.add_output(NLConditionSocket, "Positive")

    def get_netlogic_class_name(self):
        return "ULSensorPositive"

    def get_input_names(self):
        return ['obj_name', 'sens_name']

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLGetSensorNode)


class NLControllerStatus(NLConditionNode):
    bl_idname = "NLControllerStatus"
    bl_label = "Controller Status"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLLogicBrickSocket, 'Controller')
        self.inputs[-1].brick_type = 'controllers'
        self.add_output(NLConditionSocket, "Status")
        self.add_output(NLDictSocket, "Sensors")

    def get_netlogic_class_name(self):
        return "ULControllerStatus"

    def get_input_names(self):
        return ['obj_name', 'cont_name']

    def get_output_names(self):
        return ['OUT', 'SENSORS']


_nodes.append(NLControllerStatus)


class NLSetOverlayCollection(NLActionNode):
    bl_idname = "NLSetOverlayCollection"
    bl_label = "Set Overlay Collection"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLCameraSocket, 'Camera')
        self.add_input(NLCollectionSocket, 'Collection')
        self.add_output(NLConditionSocket, 'Done')

    def get_input_names(self):
        return ['condition', 'camera', 'collection']

    def get_netlogic_class_name(self):
        return "ULSetOverlayCollection"


_nodes.append(NLSetOverlayCollection)


class NLAddFilter(NLActionNode):
    bl_idname = "NLAddFilter"
    bl_label = "Add Filter"
    nl_category = "Scene"
    nl_subcat = 'Post FX'
    nl_module = 'actions'

    filter_type: EnumProperty(
        items=_enum_2d_filters,
        name='Filter',
        description='2D Filters modify the image rendered by EEVEE',
        default='FXAA',
        update=update_draw
    )

    def update_draw(self):
        self.inputs[2].enabled = self.filter_type == 'BRIGHTNESS'
        self.inputs[3].enabled = self.filter_type == 'MIST'
        self.inputs[4].enabled = self.inputs[3].enabled
        self.inputs[5].enabled = self.filter_type in ['VIGNETTE', 'CHROMAB', 'GRAYSCALE', 'MIST', 'SSAO', 'HBAO']
        self.inputs[6].enabled = self.filter_type in ['VIGNETTE', 'LEVELS', 'MIST']

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntCentSocket, 'Pass Index')
        self.add_input(NLFloatFieldSocket, 'Brightness')
        self.inputs[-1].value = 1.0
        self.add_input(NLFloatFieldSocket, 'Start')
        self.inputs[-1].value = .1
        self.add_input(NLFloatFieldSocket, 'Density')
        self.inputs[-1].value = 0.5
        self.add_input(NLFloatFieldSocket, 'Power')
        self.inputs[-1].value = 1.0
        self.add_input(NLColorSocket, 'Color')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(self, "filter_type")

    def get_input_names(self):
        return ['condition', 'pass_idx', 'brightness', 'start', 'density', 'power', 'color', 'end']

    def get_attributes(self):
        return [
            ("filter_type", lambda: f'"{self.filter_type}"')
        ]

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULAddFilter"


_nodes.append(NLAddFilter)


class NLRemoveFilter(NLActionNode):
    bl_idname = "NLRemoveFilter"
    bl_label = "Remove Filter"
    nl_category = "Scene"
    nl_subcat = 'Post FX'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntCentSocket, 'Pass Index')
        self.add_output(NLConditionSocket, 'Done')

    def get_input_names(self):
        return ['condition', 'pass_idx']

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRemoveFilter"


_nodes.append(NLRemoveFilter)


class NLToggleFilter(NLActionNode):
    bl_idname = "NLToggleFilter"
    bl_label = "Toggle Filter"
    nl_category = "Scene"
    nl_subcat = 'Post FX'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntCentSocket, 'Pass Index')
        self.add_output(NLConditionSocket, 'Done')

    def get_input_names(self):
        return ['condition', 'pass_idx']

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULToggleFilter"


_nodes.append(NLToggleFilter)


class NLSetFilterState(NLActionNode):
    bl_idname = "NLSetFilterState"
    bl_label = "Set Filter State"
    nl_category = "Scene"
    nl_subcat = 'Post FX'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntCentSocket, 'Pass Index')
        self.add_input(NLBooleanSocket, 'State')
        self.add_output(NLConditionSocket, 'Done')

    def get_input_names(self):
        return ['condition', 'pass_idx', 'state']

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetFilterState"


_nodes.append(NLSetFilterState)


class NLRemoveOverlayCollection(NLActionNode):
    bl_idname = "NLRemoveOverlayCollection"
    bl_label = "Remove Overlay Collection"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLCollectionSocket, 'Collection')
        self.add_output(NLConditionSocket, 'Done')

    def get_input_names(self):
        return ['condition', 'collection']

    def get_netlogic_class_name(self):
        return "ULRemoveOverlayCollection"


_nodes.append(NLRemoveOverlayCollection)


class NLParameterSwitchValue(NLConditionNode):
    bl_idname = "NLParameterSwitchValue"
    bl_label = "True / False"
    bl_width_min = 60
    bl_width_default = 100
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_output(NodeSocketPseudoCondition, "True")
        self.add_output(NodeSocketPseudoCondition, "False")

    def get_netlogic_class_name(self):
        return "ULTrueFalse"

    def get_input_names(self):
        return ["state"]

    def get_output_names(self):
        return ["TRUE", "FALSE"]


_nodes.append(NLParameterSwitchValue)


class NLOnInitConditionNode(NLConditionNode):
    bl_idname = "NLOnInitConditionNode"
    bl_label = "On Init"
    bl_icon = 'SORTBYEXT'
    nl_category = "Events"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_output(NLConditionSocket, "Init")

    def get_netlogic_class_name(self):
        return "ULOnInit"


_nodes.append(NLOnInitConditionNode)


class NLOnUpdateConditionNode(NLConditionNode):
    bl_idname = "NLOnUpdateConditionNode"
    bl_label = "On Update"
    bl_icon = 'TRIA_RIGHT'
    nl_category = "Events"
    nl_module = 'conditions'

    repeat: BoolProperty(update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_output(NLConditionSocket, "On Update")

    def get_netlogic_class_name(self):
        return "ULOnUpdate"


_nodes.append(NLOnUpdateConditionNode)


class NLGamepadVibration(NLParameterNode):
    bl_idname = "NLGamepadVibration"
    bl_label = "Vibration"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'actions'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntCentSocket, 'Index')
        self.add_input(NLSocketAlphaFloat, 'Left')
        self.add_input(NLSocketAlphaFloat, 'Right')
        self.add_input(NLTimeSocket, 'Time')
        self.inputs[-1].value = 1
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULGamepadVibration"

    def get_input_names(self):
        return ['condition', 'index', 'left', 'right', 'time']

    def get_output_names(self):
        return ["DONE"]


_nodes.append(NLGamepadVibration)


class NLGamepadActive(NLConditionNode):
    bl_idname = "NLGamepadActive"
    bl_label = "Gamepad Active"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLPositiveIntCentSocket, 'Index')
        self.add_output(NLConditionSocket, 'Active')

    def get_netlogic_class_name(self):
        return "ULGamepadActive"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return [utils.OUTCELL]


_nodes.append(NLGamepadActive)


class NLGamepadButtonsCondition(NLConditionNode):
    bl_idname = "NLGamepadButtonsCondition"
    bl_label = "Button Down"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'conditions'

    button: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons",
        update=update_draw
    )
    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_draw
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLPositiveIntCentSocket, 'Index')
        self.add_output(NLConditionSocket, "Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Down" if self.pulse else "Tap",
            toggle=True
        )
        layout.prop(self, "button", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadButton"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return ["BUTTON"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}'),
            ("button", lambda: f'{self.button}')
        ]


_nodes.append(NLGamepadButtonsCondition)


class NLGamepadButtonUpCondition(NLConditionNode):
    bl_idname = "NLGamepadButtonUpCondition"
    bl_label = "Button Up"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'conditions'
    button: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons",
        update=update_draw
    )
    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_draw
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLPositiveIntCentSocket, 'Index')
        self.add_output(NLConditionSocket, "Released")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Down" if self.pulse else "Tap",
            toggle=True
        )
        layout.prop(self, "button", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadButtonUp"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return ["BUTTON"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}'),
            ("button", lambda: f'{self.button}')
        ]


_nodes.append(NLGamepadButtonUpCondition)


class NLKeyboardActive(NLConditionNode):
    bl_idname = "NLKeyboardActive"
    bl_label = "Keyboard Active"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_output(NLConditionSocket, 'Active')

    def get_netlogic_class_name(self):
        return "ULKeyboardActive"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return [utils.OUTCELL]


_nodes.append(NLKeyboardActive)


class NLKeyPressedCondition(NLConditionNode):
    bl_idname = "NLKeyPressedCondition"
    bl_label = "Key Down"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'conditions'
    pulse: BoolProperty(
        description=(
            'ON: True until the key is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLKeyboardKeySocket, "")
        self.add_output(NLConditionSocket, "If Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Key Down" if self.pulse else "Key Tap",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyPressed"

    def get_input_names(self):
        return ["key_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]


_nodes.append(NLKeyPressedCondition)


class NLKeyLoggerAction(NLActionNode):
    bl_idname = "NLKeyLoggerAction"
    bl_label = "Logger"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'actions'
    pulse: BoolProperty(
        description=(
            'ON: True until the key is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_output(NLConditionSocket, "Done")
        self.add_output(NLParameterSocket, "Key Code")
        self.add_output(NLParameterSocket, "Logged Char")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Key Down" if self.pulse else "Key Tap",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyLogger"

    def get_input_names(self):
        return ["condition"]

    def get_output_names(self):
        return ["KEY_LOGGED", "KEY_CODE", "CHARACTER"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]


_nodes.append(NLKeyLoggerAction)


class NLKeyReleasedCondition(NLConditionNode):
    bl_idname = "NLKeyReleasedCondition"
    bl_label = "Key Up"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'conditions'

    pulse: BoolProperty(
        description=(
            'ON: True until the key is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=True,
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLKeyboardKeySocket, "")
        self.add_output(NLConditionSocket, "If Released")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyReleased"

    def get_input_names(self):
        return ["key_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]


_nodes.append(NLKeyReleasedCondition)


class NLMousePressedCondition(NLConditionNode):
    bl_idname = "NLMousePressedCondition"
    bl_label = "Button"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=False,
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLMouseButtonSocket, "")
        self.add_output(NLConditionSocket, "If Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMousePressed"

    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLMousePressedCondition)


class NLMouseMovedCondition(NLConditionNode):
    bl_idname = "NLMouseMovedCondition"
    bl_label = "Moved"
    bl_icon = 'MOUSE_MOVE'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=False,
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_output(NLConditionSocket, "If Moved")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMouseMoved"

    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]


_nodes.append(NLMouseMovedCondition)


class NLMouseReleasedCondition(NLConditionNode):
    bl_idname = "NLMouseReleasedCondition"
    bl_label = "Button Up"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=False,
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLMouseButtonSocket, "")
        self.add_output(NLConditionSocket, "If Released")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMouseReleased"

    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLMouseReleasedCondition)


class NLConditionOnceNode(NLConditionNode):
    bl_idname = "NLConditionOnceNode"
    bl_label = "Once"
    bl_icon = 'FF'
    nl_category = "Events"
    nl_module = 'conditions'
    advanced: BoolProperty(
        name='Offline Reset',
        description='Show Timer for when to reset if tree is inactive. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_input(NLBooleanSocket, "Repeat")
        self.add_input(NLPositiveFloatSocket, 'Reset After')
        self.inputs[-1].value = .5
        utils.register_outputs(self, NLConditionSocket, "Once")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Timer', icon='SETTINGS')

    def update_draw(self):
        if self.advanced:
            self.inputs[2].enabled = True
        else:
            self.inputs[2].enabled = False

    def get_netlogic_class_name(self):
        return "ULOnce"

    def get_input_names(self):
        return ["input_condition", 'repeat', 'reset_time']


_nodes.append(NLConditionOnceNode)


class NLObjectPropertyOperator(NLConditionNode):
    bl_idname = "NLObjectPropertyOperator"
    bl_label = "Evaluate Property"
    bl_icon = 'CON_TRANSLIKE'
    nl_module = 'conditions'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )
    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLGamePropertySocket, "Property")
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'If True')
        self.add_output(NLParameterSocket, 'Value')

    def get_netlogic_class_name(self):
        return "ULEvaluateProperty"

    def get_input_names(self):
        return [
            "game_object",
            "property_name",
            "compare_value"
        ]

    def get_attributes(self):
        return [
            ("mode", lambda: f'"{self.mode}"'),
            ("operator", lambda: f'LOGIC_OPERATORS[{self.operator}]')
        ]

    def get_output_names(self):
        return ['OUT', "VAL"]


_nodes.append(NLObjectPropertyOperator)


class NLConditionNextFrameNode(NLConditionNode):
    bl_idname = "NLConditionNextFrameNode"
    bl_label = "On Next Tick"
    bl_icon = 'FRAME_NEXT'
    nl_category = "Events"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        utils.register_inputs(self, NodeSocketPseudoCondition, "Condition")
        utils.register_outputs(self, NLConditionSocket, "Next Tick")

    def get_netlogic_class_name(self):
        return "ULOnNextTick"

    def get_input_names(self):
        return ["input_condition"]


_nodes.append(NLConditionNextFrameNode)


class NLConditionMousePressedOn(NLConditionNode):
    bl_idname = "NLConditionMousePressedOn"
    bl_label = "Button Over"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLMouseButtonSocket, "Mouse Button")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLConditionSocket, "When Pressed On")

    def get_netlogic_class_name(self):
        return "ULMousePressedOn"

    def get_input_names(self):
        return ["mouse_button", "game_object"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLConditionMousePressedOn)


class NLConditionMouseWheelMoved(NLConditionNode):
    bl_idname = "NLConditionMouseWheelMoved"
    bl_label = "Wheel"
    bl_icon = 'MOUSE_MMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'
    wheel_direction: EnumProperty(items=_enum_mouse_wheel_direction, default='3')
    deprecated = True

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLParameterSocket, '', {'enabled': False})
        self.add_output(NLConditionSocket, "When Scrolled")
        self.add_output(NLIntegerFieldSocket, "Difference")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'wheel_direction', text='')

    def get_netlogic_class_name(self):
        return "ULMouseScrolled"

    def get_input_names(self):
        return ['_old_direction']

    def get_output_names(self):
        return ['OUT', 'DIFF']

    def get_attributes(self):
        return [
            ("wheel_direction", lambda: self.wheel_direction)
        ]


_nodes.append(NLConditionMouseWheelMoved)


class NLConditionCollisionNode(NLConditionNode):
    bl_idname = "NLConditionCollisionNode"
    bl_label = "Collision"
    nl_category = "Physics"
    nl_module = 'conditions'
    pulse: BoolProperty(
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, 'Use Material')
        self.add_input(NLQuotedStringFieldSocket, "Property")
        self.add_input(NLMaterialSocket, 'Material')
        self.add_output(NLConditionSocket, "When Colliding")
        self.add_output(NLGameObjectSocket, "Colliding Object")
        self.add_output(NLListSocket, "Colliding Objects")
        self.add_output(NLVec3FieldSocket, "Point")
        self.add_output(NLVec3FieldSocket, "Normal")

    def update_draw(self):
        self.inputs[2].enabled = not self.inputs[1].value
        self.inputs[3].enabled = self.inputs[1].value

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULCollision"

    def get_input_names(self):
        return ["game_object", 'use_mat', 'prop', 'material']

    def get_output_names(self):
        return [utils.OUTCELL, "TARGET", "OBJECTS", "POINT", "NORMAL"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}'),
        ]


_nodes.append(NLConditionCollisionNode)


class NLConditionMouseTargetingNode(NLConditionNode):
    bl_idname = "NLConditionMouseTargetingNode"
    bl_label = "Over"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLConditionSocket, "On Mouse Enter")
        self.add_output(NLConditionSocket, "On Mouse Over")
        self.add_output(NLConditionSocket, "On Mouse Exit")
        self.add_output(NLParameterSocket, "Point")
        self.add_output(NLParameterSocket, "Normal")

    def get_netlogic_class_name(self):
        return "ULMouseOver"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return [
            "MOUSE_ENTERED",
            "MOUSE_OVER",
            "MOUSE_EXITED",
            "POINT",
            "NORMAL"
        ]


_nodes.append(NLConditionMouseTargetingNode)


class NLConditionAndNode(NLConditionNode):
    bl_idname = "NLConditionAndNode"
    bl_label = "And"
    bl_width_min = 60
    bl_width_default = 80
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, "A")
        self.add_input(NLConditionSocket, "B")
        self.add_output(NLConditionSocket, "If A and B")

    def get_netlogic_class_name(self):
        return "ULAnd"

    def get_input_names(self):
        return ["ca", "cb"]


_nodes.append(NLConditionAndNode)


class NLConditionAndNotNode(NLConditionNode):
    bl_idname = "NLConditionAndNotNode"
    bl_label = "And Not"
    bl_width_min = 60
    bl_width_default = 100
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, "A")
        self.add_input(NLConditionSocket, "B")
        self.add_output(NLConditionSocket, "If A and not B")

    def get_netlogic_class_name(self):
        return "ULAndNot"

    def get_input_names(self):
        return ["condition_a", "condition_b"]


_nodes.append(NLConditionAndNotNode)


class NLConditionOrNode(NLConditionNode):
    bl_idname = "NLConditionOrNode"
    bl_label = "Or"
    bl_width_min = 60
    bl_width_default = 80
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, 'A')
        self.add_input(NLConditionSocket, 'B')
        self.add_output(NLConditionSocket, 'A or B')

    def get_netlogic_class_name(self):
        return "ULOr"

    def get_input_names(self):
        return ["ca", "cb"]


_nodes.append(NLConditionOrNode)


class NLConditionOrList(NLConditionNode):
    bl_idname = "NLConditionOrList"
    bl_label = "Or List"
    bl_width_min = 60
    bl_width_default = 100
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, "A")
        self.add_input(NLConditionSocket, "B")
        self.add_input(NLConditionSocket, "C")
        self.add_input(NLConditionSocket, "D")
        self.add_input(NLConditionSocket, "E")
        self.add_input(NLConditionSocket, "F")
        self.add_output(NLConditionSocket, "Or...")

    def update_draw(self):
        for x in range(5):
            if self.inputs[x].is_linked:
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
            else:
                self.inputs[x+1].enabled = False
        if self.inputs[-1].is_linked:
            self.inputs[-1].enabled = True

    def get_netlogic_class_name(self):
        return "ULOrList"

    def get_input_names(self):
        return [
            "ca",
            "cb",
            "cc",
            "cd",
            "ce",
            "cf"
        ]


_nodes.append(NLConditionOrList)


class NLConditionAndList(NLConditionNode):
    bl_idname = "NLConditionAndList"
    bl_label = "And List"
    bl_width_min = 60
    bl_width_default = 100
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, "A")
        self.inputs[-1].default_value = "True"
        self.add_input(NLConditionSocket, "B")
        self.inputs[-1].default_value = "True"
        self.add_input(NLConditionSocket, "C")
        self.inputs[-1].default_value = "True"
        self.add_input(NLConditionSocket, "D")
        self.inputs[-1].default_value = "True"
        self.add_input(NLConditionSocket, "E")
        self.inputs[-1].default_value = "True"
        self.add_input(NLConditionSocket, "F")
        self.inputs[-1].default_value = "True"
        self.add_output(NLConditionSocket, "If All True")

    def update_draw(self):
        for x in range(5):
            if self.inputs[x].is_linked:
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
            else:
                self.inputs[x+1].enabled = False
        if self.inputs[-1].is_linked:
            self.inputs[-1].enabled = True

    def get_netlogic_class_name(self):
        return "ULAndList"

    def get_input_names(self):
        return [
            "ca",
            "cb",
            "cc",
            "cd",
            "ce",
            "cf"
        ]


_nodes.append(NLConditionAndList)


class NLConditionValueTriggerNode(NLConditionNode):
    """When input becomes trigger, sends a true signal"""
    bl_idname = "NLConditionValueTriggerNode"
    bl_label = "On Value Changed To"
    bl_icon = 'CON_TRANSLIKE'
    nl_category = "Events"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLParameterSocket, "Value")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value_type = "BOOLEAN"
        self.inputs[-1].value = "True"
        self.add_output(NLConditionSocket, "When Changed To")

    def get_netlogic_class_name(self):
        return "ULValueChangedTo"

    def get_input_names(self):
        return ["monitored_value", "trigger_value"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLConditionValueTriggerNode)


class NLConditionLogicOperation(NLConditionNode):
    bl_idname = "NLConditionLogicOperation"
    bl_label = "Compare"
    nl_category = "Math"
    nl_module = "conditions"

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLValueFieldSocket, "")
        self.add_input(NLValueFieldSocket, "")
        self.add_input(NLPositiveFloatSocket, "Threshold")
        self.add_output(NLConditionSocket, "If True")

    def update_draw(self):
        numerics = ['INTEGER', 'FLOAT']
        self.inputs[2].enabled = (
            (self.inputs[0].value_type in numerics or self.inputs[0].is_linked)
            and
            (self.inputs[1].value_type in numerics or self.inputs[1].is_linked)
        )

    def get_netlogic_class_name(self):
        return "ULCompare"

    def get_input_names(self):
        return ["param_a", "param_b", 'threshold']

    def get_attributes(self):
        return [
            ("operator", lambda: f'{self.operator}'),
        ]

    def get_output_names(self):
        return ['RESULT']


_nodes.append(NLConditionLogicOperation)


class NLConditionCompareVecs(NLConditionNode):
    bl_idname = "NLConditionCompareVecs"
    bl_label = "Compare Vectors"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'conditions'

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLXYZSocket, "")
        self.add_input(NLPositiveFloatSocket, "Threshold")
        self.add_input(NLVec3FieldSocket, "Vector A")
        self.add_input(NLVec3FieldSocket, "Vector B")
        self.add_output(NLConditionSocket, "If True")

    def get_netlogic_class_name(self):
        return "ULCompareVectors"

    def get_input_names(self):
        return ['all', 'threshold', "param_a", "param_b"]

    def get_output_names(self):
        return ['OUT']

    def get_attributes(self):
        return [
            ("operator", lambda: f'{self.operator}'),
        ]


_nodes.append(NLConditionCompareVecs)


class NLConditionDistanceCheck(NLConditionNode):
    bl_idname = "NLConditionDistanceCheck"
    bl_label = "Compare Distance"
    nl_category = "Math"
    nl_module = 'conditions'
    operation: EnumProperty(items=_enum_logic_operators)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLVec3FieldSocket, "A")
        self.add_input(NLVec3FieldSocket, "B")
        self.add_input(NLPositiveFloatSocket, "Value")
        self.add_input(NLFloatFieldSocket, "Hyst", {'enabled': False})
        self.add_output(NLConditionSocket, "Out")
        self.add_output(NLFloatFieldSocket, "Distance")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, 'operation', text='')

    def get_output_names(self):
        return ['OUT', 'DIST']

    def get_netlogic_class_name(self):
        return "ULCheckDistance"

    def get_input_names(self):
        return ["param_a", "param_b", "dist", '_old_hyst']

    def get_attributes(self):
        return [("operation", lambda: self.operation)]


_nodes.append(NLConditionDistanceCheck)


class NLConditionValueChanged(NLConditionNode):
    bl_idname = "NLConditionValueChanged"
    bl_label = "On Value Changed"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = "Events"
    nl_module = 'conditions'

    initialize: BoolProperty(
        description=(
            'When ON, skip the first change. '
            'When OFF, compare the first value to None'
        ),
        update=update_draw)

    def init(self, context):
        NLConditionNode.init(self, context)
        utils.register_inputs(self, NLParameterSocket, "Value")
        self.add_output(NLConditionSocket, "If Changed")
        self.add_output(NLParameterSocket, "Old Value")
        self.add_output(NLParameterSocket, "New Value")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "initialize",
            text="Startup" if self.initialize else "Skip Startup",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULOnValueChanged"

    def get_input_names(self):
        return ["current_value"]

    def get_attributes(self):
        return [("initialize", lambda: "True" if self.initialize else "False")]

    def get_output_names(self):
        return ['OUT', "OLD", "NEW"]


_nodes.append(NLConditionValueChanged)


class NLConditionTimeElapsed(NLConditionNode):
    bl_idname = "NLConditionTimeElapsed"
    bl_label = "Timer"
    nl_category = 'Time'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLConditionSocket, "Set Timer")
        self.add_input(NLTimeSocket, "Seconds")
        self.add_output(NLConditionSocket, "When Elapsed")

    def get_netlogic_class_name(self):
        return "ULTimer"

    def get_input_names(self):
        return ["condition", "delta_time"]


_nodes.append(NLConditionTimeElapsed)


class NLConditionNotNoneNode(NLConditionNode):
    bl_idname = "NLConditionNotNoneNode"
    bl_label = "Not None"
    bl_width_min = 60
    bl_width_default = 100
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        utils.register_inputs(self, NLParameterSocket, "Value")
        utils.register_outputs(self, NLConditionSocket, "If Not None")

    def get_netlogic_class_name(self):
        return "ULNotNone"

    def get_input_names(self):
        return ["checked_value"]


_nodes.append(NLConditionNotNoneNode)


class NLConditionNoneNode(NLConditionNode):
    bl_idname = "NLConditionNone"
    bl_label = "None"
    bl_width_min = 60
    bl_width_default = 80
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLParameterSocket, "Value")
        self.add_output(NLConditionSocket, "If None")

    def get_netlogic_class_name(self):
        return "ULNone"

    def get_input_names(self):
        return ["checked_value"]


_nodes.append(NLConditionNoneNode)


class NLConditionValueValidNode(NLConditionNode):
    bl_idname = "NLConditionValueValidNode"
    bl_label = "Value Valid"
    nl_category = "Values"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLParameterSocket, "Value")
        self.add_output(NLConditionSocket, "If Valid")

    def get_netlogic_class_name(self):
        return "ULValueValid"

    def get_input_names(self):
        return ["checked_value"]


_nodes.append(NLConditionValueValidNode)


class NLConditionNotNode(NLConditionNode):
    bl_idname = "NLConditionNotNode"
    bl_label = "Not"
    
    bl_width_min = 60
    bl_width_default = 80
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.hide = True
        self.add_input(NLConditionSocket, "Condition")
        self.add_output(NLConditionSocket, "If Not")

    def get_netlogic_class_name(self):
        return "ULNot"

    def get_input_names(self):
        return ["condition"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLConditionNotNode)


class NLConditionLogicNetworkStatusNode(NLConditionNode):
    bl_idname = "NLConditionLogitNetworkStatusNode"
    bl_label = "Logic Network Status"
    nl_category = "Logic"
    nl_subcat = 'Trees'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLSocketLogicTree, "Tree Name")
        self.add_output(NLConditionSocket, "If Running")
        self.add_output(NLConditionSocket, "If Stopped")

    def get_netlogic_class_name(self):
        return "ULLogicTreeStatus"

    def get_input_names(self):
        return ["game_object", "tree_name"]

    def get_output_names(self):
        return ["IFRUNNING", "IFSTOPPED"]


_nodes.append(NLConditionLogicNetworkStatusNode)


class NLAddObjectActionNode(NLActionNode):
    bl_idname = "NLAddObjectActionNode"
    bl_label = "Add Object"
    bl_icon = 'PLUS'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectNameSocket, "Object to Add")
        self.add_input(
            NLGameObjectSocket.bl_idname,
            "Copy Data From (Optional)"
        )
        self.add_input(NLPositiveIntegerFieldSocket, "Life")
        self.add_input(NLBooleanSocket, "Full Copy")
        self.add_output(NLConditionSocket, "Done")
        self.add_output(NLGameObjectSocket, "Added Object")

    def get_netlogic_class_name(self):
        return "ULAddObject"

    def get_input_names(self):
        return ["condition", "name", 'reference', "life", 'full_copy']

    def get_output_names(self):
        return ['OUT', 'OBJ']


_nodes.append(NLAddObjectActionNode)


class LogicNodeSpawnPool(NLActionNode):
    bl_idname = "LogicNodeSpawnPool"
    bl_label = "Spawn Pool"
    bl_icon = 'GROUP_VERTEX'
    nl_category = "Objects"
    nl_module = 'actions'

    create_on_init: BoolProperty(
        name='Startup',
        description='Create Pool on Game Start',
        default=True,
        update=update_draw
    )
    spawn_type: EnumProperty(
        items=_enum_spawn_types,
        name="Spawn Behavior",
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Create Pool")
        self.add_input(NLConditionSocket, "Spawn")
        self.add_input(NLGameObjectSocket, "Spawner")
        self.add_input(NLGameObjectNameSocket, "Object Instance")
        self.add_input(NLPositiveIntegerFieldSocket, "Amount")
        self.inputs[-1].value = 10
        self.add_input(NLPositiveIntegerFieldSocket, "Life")
        self.inputs[-1].value = 3
        self.add_input(NLPositiveFloatSocket, "Speed")
        self.inputs[-1].value = 75.0
        self.add_input(NLBooleanSocket, "Visualize")
        self.add_output(NLConditionSocket, "Pool Created")
        self.add_output(NLConditionSocket, "Spawned")
        self.add_output(NLConditionSocket, "On Hit")
        self.add_output(NLGameObjectSocket, "Hit Object")
        self.add_output(NLVectorSocket, "Hit Point")
        self.add_output(NLVectorSocket, "Hit Normal")
        self.add_output(NLVectorSocket, "Hit Direction")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'create_on_init', text='On Startup')
        layout.prop(self, 'spawn_type', text='')

    def update_draw(self):
        simple = self.spawn_type == 'Simple'
        self.inputs[0].enabled = not self.create_on_init
        self.outputs[3].enabled = not simple
        self.outputs[4].enabled = not simple
        self.outputs[5].enabled = not simple
        self.outputs[0].enabled = not self.create_on_init
        self.outputs[2].enabled = not simple
        self.outputs[3].enabled = not simple
        self.outputs[4].enabled = not simple
        self.outputs[5].enabled = not simple
        self.outputs[6].enabled = not simple

    def get_netlogic_class_name(self):
        return "ULSpawnPool"

    def get_input_names(self):
        return [
            "condition",
            'spawn',
            "spawner",
            "object_instance",
            "amount",
            "life",
            "speed",
            "visualize"
        ]

    def get_attributes(self):
        return [
            ("create_on_init", lambda: f'{self.create_on_init}'),
            ("spawn_type", lambda: f'"{self.spawn_type}"')
        ]

    def get_output_names(self):
        return ['OUT', 'SPAWNED', 'ONHIT', 'HITOBJECT', 'HITPOINT', 'HITNORMAL', 'HITDIR']


_nodes.append(LogicNodeSpawnPool)


class LogicNodeLocalServer(NLActionNode):
    bl_idname = "LogicNodeLocalServer"
    bl_label = "LAN Server"
    bl_icon = 'NETWORK_DRIVE'
    nl_category = "Network"
    nl_module = 'actions'

    on_init: BoolProperty(
        name='Startup',
        description='Start the server on game start',
        default=True,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Start")
        self.add_input(NLQuotedStringFieldSocket, "IP")
        self.inputs[-1].value = socket.gethostbyname(socket.gethostname())
        self.add_input(NLPositiveIntegerFieldSocket, "Port")
        self.inputs[-1].value = 8303
        self.add_input(NLConditionSocket, "Stop")
        self.add_output(NLConditionSocket, "Started")
        self.add_output(NLConditionSocket, "Running")
        self.add_output(NLConditionSocket, "Stopped")
        self.add_output(NLParameterSocket, "Server")
        self.add_output(NLConditionSocket, "Received")
        self.add_output(NLDictSocket, "Message")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    def get_netlogic_class_name(self):
        return "ULLocalServer"

    def get_input_names(self):
        return [
            "start_cond",
            "ip_address",
            "port",
            "stop_cond",
        ]

    def get_attributes(self):
        return [
            ("on_init", lambda: f'{self.on_init}')
        ]

    def get_output_names(self):
        return ['STARTED', 'RUNNING', 'STOPPED', 'SERVER', 'RECEIVED', 'MSG']


_nodes.append(LogicNodeLocalServer)


class LogicNodeLocalClient(NLActionNode):
    bl_idname = "LogicNodeLocalClient"
    bl_label = "LAN Client"
    bl_icon = 'RESTRICT_VIEW_OFF'
    nl_category = "Network"
    nl_module = 'actions'

    on_init: BoolProperty(
        name='Startup',
        description='Connect the client on game start',
        default=False,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Connect")
        self.add_input(NLQuotedStringFieldSocket, "IP")
        self.add_input(NLPositiveIntegerFieldSocket, "Port")
        self.inputs[-1].value = 8303
        self.add_input(NLConditionSocket, "Disconnect")
        self.add_output(NLConditionSocket, "Connect")
        self.add_output(NLConditionSocket, "Connected")
        self.add_output(NLConditionSocket, "Disconnect")
        self.add_output(NLParameterSocket, "Client")
        self.add_output(NLConditionSocket, "Received")
        self.add_output(NLDictSocket, "Message")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    def get_netlogic_class_name(self):
        return "ULLocalClient"

    def get_input_names(self):
        return [
            "connect_cond",
            "ip_address",
            "port",
            "disconnect_cond",
        ]

    def get_attributes(self):
        return [
            ("on_init", lambda: f'{self.on_init}')
        ]

    def get_output_names(self):
        return ['CONNECT', 'CONNECTED', 'DISCONNECT', 'CLIENT', 'RECEIVED', 'MSG']


_nodes.append(LogicNodeLocalClient)


class LogicNodeSendNetworkMessage(NLActionNode):
    bl_idname = "LogicNodeSendNetworkMessage"
    bl_label = "Send Data"
    bl_icon = 'OUTLINER_DATA_GP_LAYER'
    nl_category = "Network"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLParameterSocket, "Server / Client")
        self.add_input(NLParameterSocket, "Data")
        self.add_input(NLQuotedStringFieldSocket, "Subject")
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULSendNetworkMessage"

    def get_input_names(self):
        return [
            "condition",
            "entity",
            'data',
            'subject'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(LogicNodeSendNetworkMessage)


class NLSetGameObjectGamePropertyActionNode(NLActionNode):
    bl_idname = "NLSetGameObjectGamePropertyActionNode"
    bl_label = "Set Property"
    bl_icon = 'IMPORT'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGamePropertySocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_input(NLValueFieldSocket, "")
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULSetProperty"

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetGameObjectGamePropertyActionNode)


class NLSetGeometryNodeValue(NLActionNode):
    bl_idname = "NLSetGeometryNodeValue"
    bl_label = "Set Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Geometry'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGeomNodeTreeSocket, 'Tree')
        self.add_input(NLNodeGroupNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLPositiveIntegerFieldSocket, "Input")
        self.add_input(NLFloatFieldSocket, 'Value')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        tree = self.inputs[1]
        nde = self.inputs[2]
        ipt = self.inputs[3]
        val = self.inputs[4]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = val.enabled = True
        else:
            ipt.enabled = val.enabled = False
        if not tree.is_linked and not nde.is_linked and tree.value:
            tree_name = tree.value.name
            node_name = nde.value
            target = bpy.data.node_groups[tree_name].nodes[node_name]
            limit = len(target.inputs) - 1
            if int(ipt.value) > limit:
                ipt.value = limit
            name = target.inputs[ipt.value].name
            ipt.name = name

    def get_netlogic_class_name(self):
        return "ULSetNodeSocket"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetGeometryNodeValue)


class NLSetNodeTreeNodeValue(NLActionNode):
    bl_idname = "NLSetNodeTreeNodeValue"
    bl_label = "Set Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLNodeGroupSocket, 'Tree')
        self.add_input(NLNodeGroupNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLPositiveIntegerFieldSocket, "Input")
        self.add_input(NLFloatFieldSocket, 'Value')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        tree = self.inputs[1]
        nde = self.inputs[2]
        ipt = self.inputs[3]
        val = self.inputs[4]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = val.enabled = True
        else:
            ipt.enabled = val.enabled = False
        if not tree.is_linked and not nde.is_linked and tree.value:
            tree_name = tree.value.name
            node_name = nde.value
            target = bpy.data.node_groups[tree_name].nodes[node_name]
            limit = len(target.inputs) - 1
            if int(ipt.value) > limit:
                ipt.value = limit
            name = target.inputs[ipt.value].name
            ipt.name = name

    def get_netlogic_class_name(self):
        return "ULSetNodeSocket"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetNodeTreeNodeValue)


class NLSetGeometryNodeAttribute(NLActionNode):
    bl_idname = "NLSetGeometryNodeAttribute"
    bl_label = "Set Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Geometry'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGeomNodeTreeSocket, 'Tree')
        self.add_input(NLNodeGroupNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLQuotedStringFieldSocket, "Internal")
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        tree = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    def get_netlogic_class_name(self):
        return "ULSetNodeValue"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetGeometryNodeAttribute)


class NLSetNodeTreeNodeAttribute(NLActionNode):
    bl_idname = "NLSetNodeTreeNodeAttribute"
    bl_label = "Set Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLNodeGroupSocket, 'Tree')
        self.add_input(NLNodeGroupNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLQuotedStringFieldSocket, "Internal")
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        tree = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    def get_netlogic_class_name(self):
        return "ULSetNodeValue"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetNodeTreeNodeAttribute)


class NLSetMaterial(NLActionNode):
    bl_idname = "NLSetMaterial"
    bl_label = "Set Material"
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLIntegerFieldSocket, "Slot")
        self.add_input(NLMaterialSocket, "Material")
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULSetMaterial"

    def update_draw(self):
        obj_socket = self.inputs[1]
        if obj_socket.use_owner or not obj_socket.value:
            return
        if self.inputs[2].value > len(obj_socket.value.material_slots):
            self.inputs[2].value = len(obj_socket.value.material_slots)

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "slot",
            "mat_name",
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetMaterial)


class NLSetMaterialNodeValue(NLActionNode):
    bl_idname = "NLSetMaterialNodeValue"
    bl_label = "Set Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLMaterialSocket, 'Material')
        self.add_input(NLTreeNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLPositiveIntegerFieldSocket, "Input")
        self.add_input(NLFloatFieldSocket, 'Value')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        mat = self.inputs[1]
        nde = self.inputs[2]
        ipt = self.inputs[3]
        val = self.inputs[4]
        if mat.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = val.enabled = True
        else:
            ipt.enabled = val.enabled = False
        if not mat.is_linked and not nde.is_linked and mat.value:
            mat_name = mat.value.name
            node_name = nde.value
            target = bpy.data.materials[mat_name].node_tree.nodes[node_name]
            limit = len(target.inputs) - 1
            if int(ipt.value) > limit:
                ipt.value = limit
            name = target.inputs[ipt.value].name
            ipt.name = name

    def get_netlogic_class_name(self):
        return "ULSetMatNodeSocket"

    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetMaterialNodeValue)


class NLSetMaterialNodeAttribute(NLActionNode):
    bl_idname = "NLSetMaterialNodeAttribute"
    bl_label = "Set Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLMaterialSocket, 'Material')
        self.add_input(NLTreeNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLQuotedStringFieldSocket, "Internal")
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        mat = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    def get_netlogic_class_name(self):
        return "ULSetMatNodeValue"

    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetMaterialNodeAttribute)


class NLPlayMaterialSequence(NLActionNode):
    bl_idname = "NLPlayMaterialSequence"
    bl_label = "Play Sequence"
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLMaterialSocket, 'Material')
        self.add_input(NLTreeNodeSocket, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.add_input(NLPlayActionModeSocket, "Mode")
        self.inputs[-1].enabled = False
        self.add_input(NLBooleanSocket, 'Continue')
        self.inputs[-1].enabled = False
        self.add_input(NLVec2FieldSocket, "Frames")
        self.inputs[-1].enabled = False
        self.add_input(NLPositiveFloatSocket, "FPS")
        self.inputs[-1].value = 60
        self.inputs[-1].enabled = False
        self.add_output(NLConditionSocket, "On Start")
        self.add_output(NLConditionSocket, "Running")
        self.add_output(NLConditionSocket, "On Finish")
        self.add_output(NLParameterSocket, "Current Frame")

    def draw_buttons(self, context, layout):
        mat = self.inputs[1].value
        if mat:
            nde = self.inputs[2].value
            target = mat.node_tree.nodes.get(nde)
            if not isinstance(target, bpy.types.ShaderNodeTexImage):
                col = layout.column()
                col.label(text='Selected Node', icon='ERROR')
                col.label(text='not Image Texture!')

    def update_draw(self):
        mat = self.inputs[1]
        nde = self.inputs[2]
        mod = self.inputs[3]
        fra = self.inputs[5]
        fps = self.inputs[6]
        subs = [mod, fra, fps]
        target = mat.value.node_tree.nodes.get(nde.value) if mat.value else None
        valid = isinstance(target, bpy.types.ShaderNodeTexImage)
        self.inputs[4].enabled = '3' in mod.value
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked) and valid:
            for ipt in subs:
                ipt.enabled = True
        else:
            for ipt in subs:
                ipt.enabled = False

    def get_netlogic_class_name(self):
        return "ULPaySequence"

    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'play_mode',
            'play_continue',
            "frames",
            'fps'
        ]

    def get_output_names(self):
        return ['ON_START', 'RUNNING', 'ON_FINISH', 'FRAME']


_nodes.append(NLPlayMaterialSequence)


class NLToggleGameObjectGamePropertyActionNode(NLActionNode):
    bl_idname = "NLToggleGameObjectGamePropertyActionNode"
    bl_label = "Toggle Property"
    bl_icon = 'UV_SYNC_SELECT'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGamePropertySocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULToggleProperty"

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLToggleGameObjectGamePropertyActionNode)


class NLAddToGameObjectGamePropertyActionNode(NLActionNode):
    bl_idname = "NLAddToGameObjectGamePropertyActionNode"
    bl_label = "Modify Property"
    bl_icon = 'ADD'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGamePropertySocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_input(NLFloatFieldSocket, "Value")
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULModifyProperty"

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("mode", lambda: f'"{self.mode}"'),
            ("operator", lambda: f'OPERATORS.get("{self.operator}")')
        ]

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLAddToGameObjectGamePropertyActionNode)



class NLClampedModifyProperty(NLActionNode):
    bl_idname = "NLClampedModifyProperty"
    bl_label = "Clamped Modify Property"
    bl_icon = 'ARROW_LEFTRIGHT'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGamePropertySocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_input(NLFloatFieldSocket, "Value")
        self.add_input(NLVec2FieldSocket, "Range")
        self.add_output(NLConditionSocket, "Done")

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text="")

    def get_netlogic_class_name(self):
        return "ULClampedModifyProperty"

    def get_attributes(self):
        return [
            ("mode", lambda: f'"{self.mode}"'),
            ("operator", lambda: f'OPERATORS.get("{self.operator}")')
        ]

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value",
            'range'
        ]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLClampedModifyProperty)


class NLCopyPropertyFromObject(NLActionNode):
    bl_idname = "NLCopyPropertyFromObject"
    bl_label = "Copy From Object"
    bl_icon = 'PASTEDOWN'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Copy From")
        self.add_input(NLGameObjectSocket, "To")
        self.add_input(NLGamePropertySocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULCopyProperty"

    def get_input_names(self):
        return [
            "condition",
            "from_object",
            "to_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLCopyPropertyFromObject)


class NLValueSwitch(NLParameterNode):
    bl_idname = "NLValueSwitch"
    bl_label = "Value Switch"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLBooleanSocket, "A if True, else B")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = 'A'
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = 'B'
        self.add_output(NLParameterSocket, "A or B")

    def get_netlogic_class_name(self):
        return "ULValueSwitch"

    def get_input_names(self):
        return ["condition", 'val_a', 'val_b']

    def get_output_names(self):
        return ['VAL']


_nodes.append(NLValueSwitch)


class NLValueSwitchList(NLParameterNode):
    bl_idname = "NLValueSwitchList"
    bl_label = "Value Switch List"
    bl_width_min = 100
    bl_width_default = 160
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.hide = True
        self.add_input(NLBooleanSocket, "if A")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "A"
        self.add_input(NLBooleanSocket, "elif B")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "B"
        self.add_input(NLBooleanSocket, "elif C")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "C"
        self.add_input(NLBooleanSocket, "elif D")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "D"
        self.add_input(NLBooleanSocket, "elif E")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "E"
        self.add_input(NLBooleanSocket, "elif F")
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "F"
        self.add_output(NLParameterSocket.bl_idname,
                         "A or B or C or D or E or F")

    def update_draw(self):
        for x in range(0, 10, 2):
            if self.inputs[x].is_linked or self.inputs[x].value == True:
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
                self.inputs[x+2].enabled = True
            elif not self.inputs[x+1].is_linked:
                self.inputs[x+1].enabled = False
                self.inputs[x+2].enabled = False

    def get_netlogic_class_name(self):
        return "ULValueSwitchList"

    def get_input_names(self):
        return [
            "ca", 'val_a',
            "cb", 'val_b',
            "cc", 'val_c',
            "cd", 'val_d',
            "ce", 'val_e',
            "cf", 'val_f'
        ]

    def get_output_names(self):
        return ['VAL']


_nodes.append(NLValueSwitchList)


class NLValueSwitchListCompare(NLParameterNode):
    bl_idname = "NLValueSwitchListCompare"
    bl_label = "Value Switch List Compare"
    bl_width_min = 100
    bl_width_default = 172
    nl_category = "Values"
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLParameterNode.init(self, context)
        self.hide = True
        self.add_input(NLValueFieldSocket, "Switch:")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Default")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case A")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case B")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case C")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case D")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case E")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "Case F")
        self.inputs[-1].value = "_None_"
        self.add_input(NLValueFieldSocket, "")
        self.inputs[-1].value = "_None_"
        self.add_output(
            NLParameterSocket.bl_idname,
            "Output Case"
        )

    def update_draw(self):
        for x in range(2, 12):
            if self.inputs[x].is_linked or self.inputs[x].value != "_None_":
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
                self.inputs[x+2].enabled = True
            elif not self.inputs[x+1].is_linked:
                self.inputs[x+1].enabled = False
                self.inputs[x+2].enabled = False

    def get_netlogic_class_name(self):
        return "ULValueSwitchListCompare"

    def get_input_names(self):
        return [
            "p0", "val_default",
            "pa", 'val_a',
            "pb", 'val_b',
            "pc", 'val_c',
            "pd", 'val_d',
            "pe", 'val_e',
            "pf", 'val_f'
        ]

    def get_attributes(self):
        return [
            ("operator", lambda: f'{self.operator}'),
        ]

    def get_output_names(self):
        return ['RESULT']


_nodes.append(NLValueSwitchListCompare)


class NLInvertValueNode(NLParameterNode):
    bl_idname = "NLInvertValueNode"
    bl_label = "Invert"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLFloatFieldSocket, "Value")
        self.add_output(NLParameterSocket, "Value")

    def get_netlogic_class_name(self):
        return "ULInvertValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLInvertValueNode)


class NLAbsoluteValue(NLParameterNode):
    bl_idname = "NLAbsoluteValue"
    bl_label = "Absolute"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLFloatFieldSocket, "Value")
        self.add_output(NLParameterSocket, "Value")

    def get_netlogic_class_name(self):
        return "ULAbsoluteValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLAbsoluteValue)


class NLCreateVehicleFromParent(NLActionNode):
    bl_idname = "NLCreateVehicleFromParent"
    bl_label = "Create New Vehicle"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Collider")
        self.add_input(NLFloatFieldSocket, "Suspension")
        self.inputs[-1].value = 0.06
        self.add_input(NLFloatFieldSocket, "Stiffness")
        self.inputs[-1].value = 50
        self.add_input(NLFloatFieldSocket, "Damping")
        self.inputs[-1].value = 5
        self.add_input(NLFloatFieldSocket, "Friction")
        self.inputs[-1].value = 2
        self.add_input(NLPositiveFloatSocket, "Wheel Modifier")
        self.inputs[-1].value = 1
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLParameterSocket, 'Vehicle Constraint')
        self.add_output(NLListSocket, 'Wheels')

    def get_output_names(self):
        return ["OUT", 'VEHICLE', 'WHEELS']

    def get_netlogic_class_name(self):
        return "ULCreateVehicle"

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            'suspension',
            'stiffness',
            'damping',
            'friction',
            'wheel_size'
        ]


_nodes.append(NLCreateVehicleFromParent)


class NLVehicleApplyEngineForce(NLActionNode):
    bl_idname = "NLVehicleApplyEngineForce"
    bl_label = "Accelerate"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Vehicle")
        self.add_input(NLPositiveIntegerFieldSocket, "Wheels")
        self.inputs[-1].value = 2
        self.add_input(NLPositiveFloatSocket, "Power")
        self.inputs[-1].value = 1
        self.add_output(NLConditionSocket, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplyForce"

    def get_input_names(self):
        return ["condition", "vehicle", "wheelcount", 'power']

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLVehicleApplyEngineForce)


class NLVehicleApplyBraking(NLActionNode):
    bl_idname = "NLVehicleApplyBraking"
    bl_label = "Brake"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Vehicle")
        self.add_input(NLPositiveIntegerFieldSocket, "Wheels")
        self.inputs[-1].value = 2
        self.add_input(NLPositiveFloatSocket, "Power")
        self.inputs[-1].value = 1
        self.add_output(NLConditionSocket, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplyBraking"

    def get_input_names(self):
        return ["condition", "vehicle", "wheelcount", 'power']

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLVehicleApplyBraking)


class NLVehicleApplySteering(NLActionNode):
    bl_idname = "NLVehicleApplySteering"
    bl_label = "Steer"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Vehicle")
        self.add_input(NLPositiveIntegerFieldSocket, "Wheels")
        self.inputs[-1].value = 2
        self.add_input(NLFloatFieldSocket, "Steer")
        self.add_output(NLConditionSocket, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplySteering"

    def get_input_names(self):
        return ["condition", "vehicle", "wheelcount", 'power']

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLVehicleApplySteering)


class NLVehicleSetAttributes(NLActionNode):
    bl_idname = "NLVehicleSetAttributes"
    bl_label = "Set Attributes"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Collider")
        self.add_input(NLPositiveIntegerFieldSocket, "Wheels")
        self.inputs[-1].value = 2
        self.add_input(NLBooleanSocket, "Suspension")
        self.add_input(NLFloatFieldSocket, "")
        self.add_input(NLBooleanSocket, "Stiffness")
        self.add_input(NLFloatFieldSocket, "")
        self.add_input(NLBooleanSocket, "Damping")
        self.add_input(NLFloatFieldSocket, "")
        self.add_input(NLBooleanSocket, "Friction")
        self.add_input(NLFloatFieldSocket, "")
        self.add_output(NLConditionSocket, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'
        ipts = self.inputs
        ipts[4].enabled = ipts[3].value
        ipts[6].enabled = ipts[5].value
        ipts[8].enabled = ipts[7].value
        ipts[10].enabled = ipts[9].value

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleSetAttributes"

    def get_input_names(self):
        return [
            "condition",
            "vehicle",
            "wheelcount",
            'set_suspension_compression',
            'suspension_compression',
            'set_suspension_stiffness',
            'suspension_stiffness',
            'set_suspension_damping',
            'suspension_damping',
            'set_tyre_friction',
            'tyre_friction'
        ]

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLVehicleSetAttributes)


class NLSetObjectAttributeActionNode(NLActionNode):
    bl_idname = "NLSetObjectAttributeActionNode"
    bl_label = "Set Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Attribute',
        items=_enum_writable_member_names,
        update=update_draw,
        default='worldPosition'
    )
    search_tags = [
        ['Set World Position', {'value_type': 'worldPosition'}],
        ['Set World Rotation', {'value_type': 'worldOrientation'}],
        ['Set World Linear Velocity', {'value_type': 'worldLinearVelocity'}],
        ['Set World Angular Velocity', {'value_type': 'worldAngularVelocity'}],
        ['Set World Transform', {'value_type': 'worldTransform'}],
        ['Set Local Position', {'value_type': 'localPosition'}],
        ['Set Local Rotation', {'value_type': 'localOrientation'}],
        ['Set Local Linear Velocity', {'value_type': 'localLinearVelocity'}],
        ['Set Local Angular Velocity', {'value_type': 'localAngularVelocity'}],
        ['Set Local Transform', {'value_type': 'localTransform'}],
        ['Set Scale', {'value_type': 'worldScale'}],
        ['Set Color', {'value_type': 'color'}]
    ]

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLXYZSocket, "")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Value")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULSetGameObjectAttribue"

    def get_input_names(self):
        return ["condition", "xyz", "game_object", "attribute_value"]

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLSetObjectAttributeActionNode)


class NLSlowFollow(NLActionNode):
    bl_idname = "NLSlowFollow"
    bl_label = "Slow Follow"
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    value_type: EnumProperty(
        name='Attribute',
        items=_enum_writable_member_names,
        update=update_draw,
        default='worldPosition'
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGameObjectSocket, "Target")
        self.add_input(NLSocketAlphaFloat, "Factor")
        self.inputs[-1].value = .1
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULSlowFollow"

    def get_input_names(self):
        return ["condition", "game_object", "target", "factor"]

    def get_attributes(self):
        return [
            ("value_type", lambda: f'"{self.value_type}"'),
        ]


_nodes.append(NLSlowFollow)


class NLActionRayCastNode(NLActionNode):
    bl_idname = "NLActionRayCastNode"
    bl_label = "Raycast"
    nl_category = "Ray Casts"
    nl_module = 'actions'
    advanced: BoolProperty(
        name='Advanced',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLVec3FieldSocket, "Origin")
        self.add_input(NLVec3FieldSocket, "Aim")
        self.add_input(NLBooleanSocket, "Local")
        self.add_input(NLQuotedStringFieldSocket, "Property")
        self.add_input(NLMaterialSocket, "Material")
        self.add_input(NLBooleanSocket, "Exclude")
        self.add_input(NLBooleanSocket, 'X-Ray')
        self.add_input(NLBooleanSocket, "Custom Distance")
        self.add_input(NLPositiveFloatSocket, "Distance")
        self.inputs[-1].value = 100.0
        self.add_input(NLBooleanSocket, 'Visualize')
        self.add_output(NLConditionSocket, "Has Result")
        self.add_output(NLGameObjectSocket, "Picked Object")
        self.add_output(NLVec3FieldSocket, "Picked Point")
        self.add_output(NLVec3FieldSocket, "Picked Normal")
        self.add_output(NLVec3FieldSocket, "Ray Direction")
        self.add_output(NLParameterSocket, "Face Material Name")
        self.add_output(NLVec2FieldSocket, "UV Coords")
        self.update_draw()

    def update_draw(self):
        if len(self.outputs) < 7:
            return
        ipts = self.inputs
        opts = self.outputs
        adv = [
            ipts[5],
            ipts[6],
            ipts[8],
            opts[3],
            opts[4],
            opts[5],
            opts[6]
        ]
        for i in adv:
            i.enabled = self.advanced
        self.inputs[9].enabled = self.inputs[8].value and self.advanced

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_netlogic_class_name(self):
        return "ULRaycast"

    def get_attributes(self):
        return [("advanced", lambda: "True" if self.advanced else "False")]

    def get_input_names(self):
        return [
            "condition",
            "origin",
            "destination",
            'local',
            "property_name",
            "material",
            "exclude",
            'xray',
            'custom_dist',
            "distance",
            "visualize"
        ]

    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", "DIRECTION", "MATERIAL", "UV"]


_nodes.append(NLActionRayCastNode)


class NLProjectileRayCast(NLActionNode):
    bl_idname = "NLProjectileRayCast"
    bl_label = "Projectile Ray"
    nl_category = "Ray Casts"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLVec3FieldSocket, "Origin")
        self.add_input(NLVec3FieldSocket, "Aim")
        self.add_input(NLBooleanSocket, 'Local')
        self.add_input(NLPositiveFloatSocket, "Power")
        self.inputs[-1].value = 10.0
        self.add_input(NLPositiveFloatSocket, "Distance")
        self.inputs[-1].value = 20.0
        self.add_input(NLSocketAlphaFloat, "Resolution")
        self.inputs[-1].value = 0.9
        self.add_input(NLQuotedStringFieldSocket, "Property")
        self.add_input(NLBooleanSocket, 'X-Ray')
        self.add_input(NLBooleanSocket, 'Visualize')
        self.add_output(NLConditionSocket, "Has Result")
        self.add_output(NLGameObjectSocket, "Picked Object")
        self.add_output(NLVec3FieldSocket, "Picked Point")
        self.add_output(NLVec3FieldSocket, "Picked Normal")
        self.add_output(NLListSocket, "Parabola")

    def get_netlogic_class_name(self):
        return "ULProjectileRayCast"

    def get_input_names(self):
        return [
            "condition",
            "origin",
            "destination",
            'local',
            'power',
            'distance',
            "resolution",
            "property_name",
            'xray',
            "visualize"
        ]

    def get_output_names(self):
        return [utils.OUTCELL, "PICKED_OBJECT", "POINT", "NORMAL", 'PARABOLA']


_nodes.append(NLProjectileRayCast)


# TODO: should we reset conditions that have been consumed?
# Like a "once" condition. I'd say no.
class NLStartLogicNetworkActionNode(NLActionNode):
    bl_idname = "NLStartLogicNetworkActionNode"
    bl_label = "Start Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLSocketLogicTree, 'Tree Name')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStartSubNetwork"

    def get_input_names(self):
        return ["condition", "game_object", "logic_network_name"]


_nodes.append(NLStartLogicNetworkActionNode)


class NLStopLogicNetworkActionNode(NLActionNode):
    bl_idname = "NLStopLogicNetworkActionNode"
    bl_label = "Stop Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLSocketLogicTree, 'Tree Name')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStopSubNetwork"

    def get_input_names(self):
        return ["condition", "game_object", "logic_network_name"]


_nodes.append(NLStopLogicNetworkActionNode)


class NLActionSetGameObjectVisibility(NLActionNode):
    bl_idname = "NLActionSetGameObjectVisibility"
    bl_label = "Set Visibility"
    bl_icon = 'HIDE_OFF'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, "Visible")
        socket = self.inputs[-1]
        socket.use_toggle = True
        socket.true_label = "Visible"
        socket.false_label = "Not Visibile"
        self.add_input(NLBooleanSocket, "Include Children")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetVisibility"

    def get_input_names(self):
        return ["condition", "game_object", "visible", "recursive"]


_nodes.append(NLActionSetGameObjectVisibility)


class NLActionSetCollectionVisibility(NLActionNode):
    bl_idname = "NLActionSetCollectionVisibility"
    bl_label = "Set Collection Visibility"
    bl_icon = 'HIDE_OFF'
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLCollectionSocket, "Collection")
        self.add_input(NLBooleanSocket, "Visible")
        socket = self.inputs[-1]
        socket.use_toggle = True
        socket.true_label = "Visible"
        socket.false_label = "Not Visibile"
        self.add_input(NLBooleanSocket, "Include Children")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollectionVisibility"

    def get_input_names(self):
        return ["condition", "collection", "visible", "recursive"]


_nodes.append(NLActionSetCollectionVisibility)


class NLSetCurvePoints(NLActionNode):
    bl_idname = "NLSetCurvePoints"
    bl_label = "Set Curve Points"
    bl_icon = 'OUTLINER_DATA_CURVE'
    nl_category = "Objects"
    nl_subcat = 'Curves'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLCurveObjectSocket, "Curve")
        self.add_input(NLListSocket, "Points")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCurvePoints"

    def get_input_names(self):
        return ["condition", "curve_object", "points"]


_nodes.append(NLSetCurvePoints)


class NLActionFindObjectNode(NLParameterNode):
    bl_idname = "NLActionFindObjectNode"
    bl_label = "Get Object"
    bl_icon = 'OBJECT_DATA'
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLGameObjectSocket, "Object")

    def get_netlogic_class_name(self):
        return "ULGetObject"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLActionFindObjectNode)


class NLActionSendMessage(NLActionNode):
    bl_idname = "NLActionSendMessage"
    bl_label = "Send Message"
    bl_icon = 'OBJECT_DATA'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "From")
        self.add_input(NLGameObjectNameSocket, "To")
        self.add_input(NLQuotedStringFieldSocket, "Subject")
        self.add_input(NLQuotedStringFieldSocket, "Body")
        self.add_output(NLConditionSocket, "Done")

    def get_netlogic_class_name(self):
        return "ULSendMessage"

    def get_input_names(self):
        return ['condition', 'from_obj', 'to_obj', 'subject', 'body']

    def get_output_names(self):
        return [utils.OUTCELL]


_nodes.append(NLActionSendMessage)


class NLActionSetActiveCamera(NLActionNode):
    bl_idname = "NLActionSetActiveCamera"
    bl_label = "Set Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Camera')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCamera"

    def get_input_names(self):
        return ["condition", "camera"]


_nodes.append(NLActionSetActiveCamera)


class NLActionSetCameraFov(NLActionNode):
    bl_idname = "NLActionSetCameraFov"
    bl_label = "Set FOV"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Camera')
        self.add_input(NLFloatFieldSocket, 'FOV')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCameraFOV"

    def get_input_names(self):
        return ["condition", "camera", 'fov']


_nodes.append(NLActionSetCameraFov)


class NLActionSetCameraOrthoScale(NLActionNode):
    bl_idname = "NLActionSetCameraOrthoScale"
    bl_label = "Set Orthographic Scale"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Camera')
        self.add_input(NLFloatFieldSocket, 'Scale')
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCameraOrthoScale"

    def get_input_names(self):
        return ["condition", "camera", 'scale']


_nodes.append(NLActionSetCameraOrthoScale)


class NLActionSetResolution(NLActionNode):
    bl_idname = "NLActionSetResolution"
    bl_label = "Set Resolution"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLIntegerFieldSocket, 'X')
        self.inputs[-1].value = 1920
        self.add_input(NLIntegerFieldSocket, 'Y')
        self.inputs[-1].value = 1080
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetResolution"

    def get_input_names(self):
        return ["condition", "x_res", 'y_res']


_nodes.append(NLActionSetResolution)


class NLActionSetFullscreen(NLActionNode):
    bl_idname = "NLActionSetFullscreen"
    bl_label = "Set Fullscreen"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Fullscreen')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetFullscreen"

    def get_input_names(self):
        return ["condition", "use_fullscreen"]


_nodes.append(NLActionSetFullscreen)


class NLSetProfile(NLActionNode):
    bl_idname = "NLSetProfile"
    bl_label = "Show Profile"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Show')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetProfile"

    def get_input_names(self):
        return ["condition", "use_profile"]


_nodes.append(NLSetProfile)


class NLShowFramerate(NLActionNode):
    bl_idname = "NLShowFramerate"
    bl_label = "Show Framerate"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Show')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULShowFramerate"

    def get_input_names(self):
        return ["condition", "use_framerate"]


_nodes.append(NLShowFramerate)


class NLActionSetVSync(NLActionNode):
    bl_idname = "NLActionSetVSync"
    bl_label = "Set VSync"
    nl_category = 'Render'
    nl_module = 'actions'
    vsync_mode: EnumProperty(items=_enum_vsync_modes)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'vsync_mode', text='')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetVSync"

    def get_attributes(self):
        return [
            ('vsync_mode', lambda: self.vsync_mode)
        ]

    def get_input_names(self):
        return ["condition"]


_nodes.append(NLActionSetVSync)


class NLInitEmptyDict(NLParameterNode):
    bl_idname = "NLInitEmptyDict"
    bl_label = "Create Empty"
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_output(NLDictSocket, 'Dictionary')

    def get_output_names(self):
        return ['DICT']

    def get_netlogic_class_name(self):
        return "ULInitEmptyDict"


_nodes.append(NLInitEmptyDict)


class NLInitNewDict(NLParameterNode):
    bl_idname = "NLInitNewDict"
    bl_label = "Create From Item"
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, 'Key')
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLDictSocket, 'Dictionary')

    def get_output_names(self):
        return ['DICT']

    def get_netlogic_class_name(self):
        return "ULInitNewDict"

    def get_input_names(self):
        return ['key', 'val']


_nodes.append(NLInitNewDict)


class NLSetDictKeyValue(NLActionNode):
    bl_idname = "NLSetDictKeyValue"
    bl_label = "Set Key"
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLDictSocket, 'Dictionary')
        self.add_input(NLQuotedStringFieldSocket, 'Key')
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLDictSocket, 'Dictionary')

    def get_output_names(self):
        return ["OUT", "DICT"]

    def get_netlogic_class_name(self):
        return "ULSetDictKey"

    def get_input_names(self):
        return ["condition", 'dict', 'key', 'val']


_nodes.append(NLSetDictKeyValue)


class NLSetDictDelKey(NLActionNode):
    bl_idname = "NLSetDictDelKey"
    bl_label = "Remove Key"
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLDictSocket, 'Dictionary')
        self.add_input(NLQuotedStringFieldSocket, 'Key')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLDictSocket, 'Dictionary')
        self.add_output(NLParameterSocket, 'Value')

    def get_output_names(self):
        return ["OUT", "DICT", 'VALUE']

    def get_netlogic_class_name(self):
        return "ULPopDictKey"

    def get_input_names(self):
        return ["condition", 'dict', 'key']


_nodes.append(NLSetDictDelKey)


class NLInitEmptyList(NLParameterNode):
    bl_idname = "NLInitEmptyList"
    bl_label = "Create Empty"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLIntegerFieldSocket, 'Length')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ['LIST']

    def get_netlogic_class_name(self):
        return "ULInitEmptyList"

    def get_input_names(self):
        return ['length']


_nodes.append(NLInitEmptyList)


class NLInitNewList(NLParameterNode):
    bl_idname = "NLInitNewList"
    bl_label = "Create From Items"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLListItemSocket, 'Item')
        self.add_input(NLListItemSocket, 'Item')
        self.add_output(NLListSocket, 'List')

    def draw_buttons(self, context, layout):
        layout.operator(bge_netlogic.ops.NLAddListItemSocket.bl_idname)

    def set_new_input_name(self):
        self.inputs[-1].name = 'Item'

    def setup(
        self,
        cell_varname,
        uids
    ):
        items = ''
        for socket in self.inputs:
            field_value = None
            if socket.is_linked:
                field_value = self.get_linked_socket_field_value(
                    socket,
                    cell_varname,
                    None,
                    uids
                )
            else:
                field_value = socket.get_unlinked_value()
            items += f'{field_value}, '
        items = items[:-2]
        return f'        {cell_varname}.items = [{items}]\n'

    def get_output_names(self):
        return ['LIST']

    def get_netlogic_class_name(self):
        return "ULListFromItems"


_nodes.append(NLInitNewList)


class NLExtendList(NLParameterNode):
    bl_idname = "NLExtendList"
    bl_label = "Extend"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'actions'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLListSocket, 'List 1')
        self.add_input(NLListSocket, 'List 2')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULExtendList"

    def get_input_names(self):
        return ['list_1', 'list_2']


_nodes.append(NLExtendList)


class NLAppendListItem(NLActionNode):
    bl_idname = "NLAppendListItem"
    bl_label = "Append"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLListSocket, 'List')
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULAppendListItem"

    def get_input_names(self):
        return ["condition", 'items', 'val']


_nodes.append(NLAppendListItem)


class NLSetListIndex(NLActionNode):
    bl_idname = "NLSetListIndex"
    bl_label = "Set Index"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLListSocket, 'List')
        self.add_input(NLIntegerFieldSocket, 'Index')
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULSetListIndex"

    def get_input_names(self):
        return ["condition", 'items', 'index', 'val']


_nodes.append(NLSetListIndex)


class NLRemoveListValue(NLActionNode):
    bl_idname = "NLRemoveListValue"
    bl_label = "Remove Value"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLListSocket, 'List')
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULRemoveListValue"

    def get_input_names(self):
        return ["condition", 'items', 'val']


_nodes.append(NLRemoveListValue)


class NLRemoveListIndex(NLActionNode):
    bl_idname = "NLRemoveListIndex"
    bl_label = "Remove Index"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLListSocket, 'List')
        self.add_input(NLIntegerFieldSocket, 'Index')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULRemoveListIndex"

    def get_input_names(self):
        return ["condition", 'items', 'idx']


_nodes.append(NLRemoveListIndex)


class NLActionInstallSubNetwork(NLActionNode):
    bl_idname = "NLActionInstallSubNetwork"
    bl_label = "Add Logic Tree to Object"
    nl_category = "Logic"
    nl_subcat = 'Trees'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Target Object")
        self.add_input(NLSocketLogicTree, "Tree Name")
        self.add_input(NLBooleanSocket, "Initialize")
        self.inputs[-1].use_toggle = True
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULInstallSubNetwork"

    def get_input_names(self):
        return ["condition", "target_object", "tree_name", "initial_status"]


_nodes.append(NLActionInstallSubNetwork)


class NLActionExecuteNetwork(NLActionNode):
    bl_idname = "NLActionExecuteNetwork"
    bl_label = "Execute Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_input(NLGameObjectSocket, "Target Object")
        self.add_input(NLSocketLogicTree, "Tree Name")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULExecuteSubNetwork"

    def get_input_names(self):
        return ["condition", "target_object", "tree_name"]


_nodes.append(NLActionExecuteNetwork)


class NLActionStopAnimation(NLActionNode):
    bl_idname = "NLActionStopAnimation"
    bl_label = "Stop Animation"
    nl_category = "Animation"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(
            NLPositiveIntegerFieldSocket.bl_idname,
            "Animation Layer"
        )
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStopAction"

    def get_input_names(self):
        return ["condition", "game_object", "action_layer"]


_nodes.append(NLActionStopAnimation)


class NLActionSetAnimationFrame(NLActionNode):
    bl_idname = "NLActionSetAnimationFrame"
    bl_label = "Set Animation Frame"
    nl_category = "Animation"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NodeSocketLogicAnimation, "Action")
        self.add_input(NLPositiveIntegerFieldSocket, "Layer")
        self.add_input(NLPositiveFloatSocket, "Frame")
        self.add_input(NLBooleanSocket, "Freeze")
        self.inputs[-1].value = True
        self.add_input(NLSocketAlphaFloat, "Layer Weight")
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetActionFrame"

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "action_layer",
            "action_frame",
            'freeze',
            'layer_weight'
        ]


_nodes.append(NLActionSetAnimationFrame)


class NLActionApplyLocation(NLActionNode):
    bl_idname = "NLActionApplyLocation"
    bl_label = "Apply Movement"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULApplyMovement"

    def get_input_names(self):
        return ["condition", "game_object", "movement"]

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyLocation)


class NLActionApplyRotation(NLActionNode):
    bl_idname = "NLActionApplyRotation"
    bl_label = "Apply Rotation"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLVec3RotationSocket, 'Vector')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULApplyRotation"

    def get_input_names(self):
        return ["condition", "game_object", "rotation"]

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyRotation)


class NLActionApplyForce(NLActionNode):
    bl_idname = "NLActionApplyForce"
    bl_label = "Apply Force"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector"
        )
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULApplyForce"

    def get_input_names(self):
        return ["condition", "game_object", "force"]

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyForce)


class NLActionApplyImpulse(NLActionNode):
    bl_idname = "NLActionApplyImpulse"
    bl_label = "Apply Impulse"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=False, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLVec3FieldSocket, 'Point')
        self.add_input(NLVec3FieldSocket, 'Direction')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULApplyImpulse"

    def get_input_names(self):
        return ["condition", "game_object", "point", 'impulse']

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyImpulse)


class NLGamepadLook(NLActionNode):
    bl_idname = "NLGamepadLook"
    bl_label = "Gamepad Look"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'actions'
    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Main Object')
        self.add_input(NLGameObjectSocket, 'Head Object (Optional)')
        self.add_input(NLInvertedXYSocket, 'Inverted')
        self.inputs[-1].x = True
        self.add_input(NLPositiveIntCentSocket, 'Index')
        self.add_input(NLPositiveFloatSocket, 'Sensitivity')
        self.inputs[-1].value = .25
        self.add_input(NLPositiveFloatSocket, 'Exponent')
        self.inputs[-1].value = 2.3
        self.add_input(NLBooleanSocket, 'Cap Left / Right')
        self.add_input(NLAngleLimitSocket, '')
        self.add_input(NLBooleanSocket, 'Cap Up / Down')
        self.add_input(NLAngleLimitSocket, '')
        self.inputs[-1].value_x = math.radians(89)
        self.inputs[-1].value_y = math.radians(89)
        self.add_input(NLPositiveFloatSocket, 'Threshold')
        self.inputs[-1].value = 0.1
        self.add_output(NLConditionSocket, "Done")

    def update_draw(self):
        if len(self.inputs) < 12:
            return
        ipts = self.inputs
        ipts[8].enabled = ipts[7].value
        ipts[10].enabled = ipts[9].value

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadLook"

    def get_input_names(self):
        return [
            'condition',
            'main_obj',
            'head_obj',
            'inverted',
            "index",
            'sensitivity',
            'exponent',
            'use_cap_x',
            'cap_x',
            'use_cap_y',
            'cap_y',
            'threshold'
        ]

    def get_output_names(self):
        return ["DONE"]

    def get_attributes(self):
        return [
            ("axis", lambda: f'{self.axis}'),
        ]


_nodes.append(NLGamepadLook)


class NLUILayout(NLParameterNode):
    bl_idname = "NLUILayout"
    bl_label = "Layout"
    nl_category = "UI"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, 'Name')
        self.add_output(NLParameterSocket, 'Layout')
        self.add_output(NLListSocket, 'Widgets')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULUILayout"

    def get_input_names(self):
        return ["condition", "game_object"]


# _nodes.append(NLUILayout)


class NLSetCollisionGroup(NLActionNode):
    bl_idname = "NLSetCollisionGroup"
    bl_label = "Set Collision Group"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLCollisionMaskSocket, 'Group')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollisionGroup"

    def get_input_names(self):
        return ["condition", "game_object", 'slots']


_nodes.append(NLSetCollisionGroup)


class NLSetCollisionMask(NLActionNode):
    bl_idname = "NLSetCollisionMask"
    bl_label = "Set Collision Mask"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLCollisionMaskSocket, 'Mask')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollisionMask"

    def get_input_names(self):
        return ["condition", "game_object", 'slots']


_nodes.append(NLSetCollisionMask)


class NLActionCharacterJump(NLActionNode):
    bl_idname = "NLActionCharacterJump"
    bl_label = "Jump"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULCharacterJump"

    def get_input_names(self):
        return ["condition", "game_object"]


_nodes.append(NLActionCharacterJump)


class NLSetCharacterJumpSpeed(NLActionNode):
    bl_idname = "NLSetCharacterJumpSpeed"
    bl_label = "Set Jump Force"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLGameObjectSocket, 'Object')
        self.add_input(NLPositiveFloatSocket, 'Force')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterJumpSpeed"

    def get_input_names(self):
        return ["condition", "game_object", "force"]


_nodes.append(NLSetCharacterJumpSpeed)


class NLActionSaveGame(NLActionNode):
    bl_idname = "NLActionSaveGame"
    bl_label = "Save Game"
    bl_icon = 'FILE_TICK'
    nl_category = "Game"
    nl_module = 'actions'
    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='FILE_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntegerFieldSocket, 'Slot')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Saves",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULSaveGame"

    def get_input_names(self):
        return ["condition", 'slot']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionSaveGame)


class NLActionLoadGame(NLActionNode):
    bl_idname = "NLActionLoadGame"
    bl_label = "Load Game"
    bl_icon = 'FILE_FOLDER'
    nl_category = "Game"
    nl_module = 'actions'
    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='FILE_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveIntegerFieldSocket, 'Slot')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Saves",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULLoadGame"

    def get_input_names(self):
        return ["condition", 'slot']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionLoadGame)


class NLActionSaveVariable(NLActionNode):
    bl_idname = "NLActionSaveVariable"
    bl_label = "Save Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_input(NLQuotedStringFieldSocket, 'Variable')
        self.inputs[-1].value = 'var'
        self.add_input(NLValueFieldSocket, '')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        r = layout.row()
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULSaveVariable"

    def get_input_names(self):
        return ["condition", 'file_name', 'name', 'val']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionSaveVariable)


class NLActionSaveVariables(NLActionNode):
    bl_idname = "NLActionSaveVariables"
    bl_label = "Save Variable Dict"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_input(NLDictSocket, 'Variables')
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        r = layout.row()
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULSaveVariableDict"

    def get_input_names(self):
        return ["condition", 'file_name', 'val']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionSaveVariables)


class NLSetScene(NLActionNode):
    bl_idname = "NLSetScene"
    bl_label = "Set Scene"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLSceneSocket, "Scene")
        self.add_output(NLConditionSocket, 'Done')

    def get_netlogic_class_name(self):
        return "ULSetScene"

    def get_input_names(self):
        return ['condition', 'scene']

    def get_output_names(self):
        return ['OUT']


_nodes.append(NLSetScene)


class NLLoadScene(NLActionNode):
    bl_idname = "NLLoadScene"
    bl_label = "Load Scene"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLSceneSocket, "Scene")
        self.add_output(NLConditionSocket, 'Loaded')
        self.add_output(NLConditionSocket, 'Updated')
        self.add_output(NLParameterSocket, 'Status')
        self.add_output(NLParameterSocket, 'Datatype')
        self.add_output(NLParameterSocket, 'Item')

    def get_netlogic_class_name(self):
        return "ULLoadScene"

    def get_input_names(self):
        return ['condition', 'scene']

    def get_output_names(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']


_nodes.append(NLLoadScene)


class NLLoadFileContent(NLActionNode):
    bl_idname = "NLLoadFileContent"
    bl_label = "Load File Content"
    nl_category = "File"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_output(NLConditionSocket, 'Loaded')
        self.add_output(NLConditionSocket, 'Updated')
        self.add_output(NLParameterSocket, 'Status')
        self.add_output(NLParameterSocket, 'Datatype')
        self.add_output(NLParameterSocket, 'Item')

    def get_netlogic_class_name(self):
        return "ULLoadFileContent"

    def get_input_names(self):
        return ['condition']

    def get_output_names(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']


_nodes.append(NLLoadFileContent)


class NLParameterSetAttribute(NLActionNode):
    bl_idname = "NLParameterSetAttribute"
    bl_label = "Set Object Attribute"
    nl_category = "Python"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPythonSocket, "Object Instance")
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, "")

    def get_netlogic_class_name(self):
        return "ULSetPyInstanceAttr"

    def get_input_names(self):
        return ['condition', 'instance', 'attr', 'value']


_nodes.append(NLParameterSetAttribute)


class NLActionLoadVariable(NLActionNode):
    bl_idname = "NLActionLoadVariable"
    bl_label = "Load Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'parameters'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_input(NLQuotedStringFieldSocket, 'Name')
        self.inputs[-1].value = 'var'
        self.add_input(NLOptionalValueFieldSocket, 'Default Value')
        self.add_output(NLParameterSocket, 'Value')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULLoadVariable"

    def get_input_names(self):
        return ['file_name', 'name', 'default_value']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ['VAR']


_nodes.append(NLActionLoadVariable)


class NLActionLoadVariables(NLActionNode):
    bl_idname = "NLActionLoadVariables"
    bl_label = "Load Variable Dict"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'parameters'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_output(NLDictSocket, 'Variables')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULLoadVariableDict"

    def get_input_names(self):
        return ["file_name", 'name']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["VAR"]


_nodes.append(NLActionLoadVariables)


class NLActionRemoveVariable(NLActionNode):
    bl_idname = "NLActionRemoveVariable"
    bl_label = "Remove Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_input(NLQuotedStringFieldSocket, 'Name')
        self.inputs[-1].value = 'var'
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULRemoveVariable"

    def get_input_names(self):
        return ["condition", 'file_name', 'name']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionRemoveVariable)


class NLActionClearVariables(NLActionNode):
    bl_idname = "NLActionClearVariables"
    bl_label = "Clear Variables"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULClearVariables"

    def get_input_names(self):
        return ["condition", 'file_name']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLActionClearVariables)


class NLActionListVariables(NLActionNode):
    bl_idname = "NLActionListVariables"
    bl_label = "List Saved Variables"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_draw)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_draw,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, 'Condition')
        self.add_input(NLQuotedStringFieldSocket, 'Filename')
        self.inputs[-1].value = 'variables'
        self.add_input(NLBooleanSocket, 'Print')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLListSocket, 'List')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_netlogic_class_name(self):
        return "ULListVariables"

    def get_input_names(self):
        return ["condition", 'file_name', 'print_list']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            lambda: "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT", 'LIST']


_nodes.append(NLActionListVariables)


class NLActionSetCharacterJump(NLActionNode):
    bl_idname = "NLSetActionCharacterJump"
    bl_label = "Set Max Jumps"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLPositiveIntegerFieldSocket, "Max Jumps")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterMaxJumps"

    def get_input_names(self):
        return ["condition", "game_object", 'max_jumps']


_nodes.append(NLActionSetCharacterJump)


class NLActionSetCharacterGravity(NLActionNode):
    bl_idname = "NLActionSetCharacterGravity"
    bl_label = "Set Gravity"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVelocitySocket, "Gravity")
        self.inputs[-1].value_z = -9.8
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterGravity"

    def get_input_names(self):
        return ["condition", "game_object", 'gravity']


_nodes.append(NLActionSetCharacterGravity)


class NLActionSetCharacterWalkDir(NLActionNode):
    bl_idname = "NLActionSetCharacterWalkDir"
    bl_label = "Walk"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Vector")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULSetCharacterWalkDir"

    def get_input_names(self):
        return ["condition", "game_object", 'walkDir']

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionSetCharacterWalkDir)


class NLActionSetCharacterVelocity(NLActionNode):
    bl_idname = "NLActionSetCharacterVelocity"
    bl_label = "Set Velocity"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Velocity")
        self.add_input(NLPositiveFloatSocket, "Time")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULSetCharacterVelocity"

    def get_input_names(self):
        return ["condition", "game_object", 'vel', 'time']

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionSetCharacterVelocity)


class NLActionApplyTorque(NLActionNode):
    bl_idname = "NLActionApplyTorque"
    bl_label = "Apply Torque"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULApplyTorque"

    def get_input_names(self):
        return ["condition", "game_object", "torque"]

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyTorque)


class NLActionEndObjectNode(NLActionNode):
    bl_idname = "NLActionEndObjectNode"
    bl_label = "Remove Object"
    bl_icon = 'TRASH'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULEndObject"

    def get_input_names(self):
        return ["condition", "game_object"]


_nodes.append(NLActionEndObjectNode)


class NLActionSetTimeScale(NLActionNode):
    bl_idname = "NLActionSetTimeScale"
    bl_label = "Set Timescale"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLPositiveFloatSocket, "Timescale")
        self.inputs[-1].value = 1
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetTimeScale"

    def get_input_names(self):
        return ["condition", "timescale"]


_nodes.append(NLActionSetTimeScale)


class NLActionSetGravity(NLActionNode):
    bl_idname = "NLActionSetGravity"
    bl_label = "Set Gravity"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLVelocitySocket, "Gravity")
        self.inputs[-1].value_z = -9.8
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetGravity"

    def get_input_names(self):
        return ["condition", "gravity"]


_nodes.append(NLActionSetGravity)


class NLActionReplaceMesh(NLActionNode):
    bl_idname = "NLActionReplaceMesh"
    bl_label = "Replace Mesh"
    bl_icon = 'MESH_DATA'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLMeshSocket, "New Mesh Name")
        self.add_input(NLBooleanSocket, "Use Display")
        self.add_input(NLBooleanSocket, "Use Physics")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULReplaceMesh"

    def get_input_names(self):
        return [
            "condition",
            "target_game_object",
            "new_mesh_name",
            "use_display",
            "use_physics"
        ]


_nodes.append(NLActionReplaceMesh)


class NLActionRemovePhysicsConstraint(NLActionNode):
    bl_idname = "NLActionRemovePhysicsConstraint"
    bl_label = "Remove Constraint"
    bl_icon = 'TRASH'
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLQuotedStringFieldSocket, "Name")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRemovePhysicsConstraint"

    def get_input_names(self):
        return ["condition", "object", "name"]


_nodes.append(NLActionRemovePhysicsConstraint)


class NLActionAddPhysicsConstraint(NLActionNode):
    bl_idname = "NLActionAddPhysicsConstraint"
    bl_label = "Add Constraint"
    bl_icon = 'CONSTRAINT'
    nl_category = "Physics"
    nl_module = 'actions'
    constraint: EnumProperty(items=_enum_constraint_types, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLGameObjectSocket, "Target")
        self.add_input(NLQuotedStringFieldSocket, 'Name')
        self.add_input(NLBooleanSocket, 'Use World Space')
        self.add_input(NLVec3FieldSocket, 'Pivot')
        self.add_input(NLBooleanSocket, 'Limit Axis')
        self.add_input(NLVec3FieldSocket, 'Axis Limits')
        self.add_input(NLBooleanSocket, 'Linked Collision')
        self.inputs[-1].value = True
        self.add_output(NLConditionSocket, 'Done')
        self.update_draw()

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'constraint', text='')

    def update_draw(self):
        if len(self.inputs) < 9:
            return
        if self.constraint == 'bge.constraints.POINTTOPOINT_CONSTRAINT':
            self.inputs[6].enabled = False
            self.inputs[7].enabled = False
            return
        else:
            self.inputs[6].enabled = True
        if not self.inputs[6].value:
            self.inputs[7].enabled = False
        else:
            self.inputs[7].enabled = True

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULAddPhysicsConstraint"

    def get_attributes(self):
        return [
            ('constraint', lambda: self.constraint)
        ]

    def get_input_names(self):
        return [
            "condition",
            "target",
            "child",
            "name",
            'use_world',
            "pivot",
            'use_limit',
            "axis_limits",
            "linked_col"
        ]


_nodes.append(NLActionAddPhysicsConstraint)


class NLSetGammaAction(NLActionNode):
    bl_idname = "NLSetGammaAction"
    bl_label = "Set Gamma"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveFloatSocket, 'Gamma')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetGamma"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetGammaAction)


class NLSetExposureAction(NLActionNode):
    bl_idname = "NLSetExposureAction"
    bl_label = "Set Exposure"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLPositiveFloatSocket, 'Exposure')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetExposure"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetExposureAction)


class NLSetEeveeAO(NLActionNode):
    bl_idname = "NLSetEeveeAO"
    bl_label = "Set Ambient Occlusion"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Use AO')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeAO"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeAO)


class NLSetEeveeBloom(NLActionNode):
    bl_idname = "NLSetEeveeBloom"
    bl_label = "Set Bloom"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Use Bloom')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeBloom"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeBloom)


class NLSetEeveeSSR(NLActionNode):
    bl_idname = "NLSetEeveeSSR"
    bl_label = "Set SSR"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Use SSR')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSSR"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeSSR)


class NLSetEeveeVolumetrics(NLActionNode):
    bl_idname = "NLSetEeveeVolumetrics"
    bl_label = "Set Volumetric Light"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Volumetrics')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeVolumetrics"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeVolumetrics)


class NLSetEeveeSMAA(NLActionNode):
    bl_idname = "NLSetEeveeSMAA"
    bl_label = "Set SMAA"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'
    deprecated = True

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLBooleanSocket, 'Use SMAA')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSMAA"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeSMAA)



class NLSetLightEnergyAction(NLActionNode):
    bl_idname = "NLSetLightEnergyAction"
    bl_label = "Set Light Energy"
    nl_category = "Lights"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLLightObjectSocket, 'Light Object')
        self.add_input(NLFloatFieldSocket, 'Energy')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightEnergy"

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "energy"
        ]


_nodes.append(NLSetLightEnergyAction)


class NLMakeUniqueLight(NLActionNode):
    bl_idname = "NLMakeUniqueLight"
    bl_label = "Make Unique"
    nl_category = "Lights"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLLightObjectSocket, 'Light Object')
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLLightObjectSocket, 'Light')

    def get_output_names(self):
        return ["OUT", 'LIGHT']

    def get_netlogic_class_name(self):
        return "ULMakeUniqueLight"

    def get_input_names(self):
        return [
            "condition",
            "light",
        ]


_nodes.append(NLMakeUniqueLight)


class NLSetLightShadowAction(NLActionNode):
    bl_idname = "NLSetLightShadowAction"
    bl_label = "Set Light Shadow"
    nl_category = "Lights"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLLightObjectSocket, 'Light Object')
        self.add_input(NLBooleanSocket, 'Use Shadow')
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightShadow"

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "use_shadow"
        ]


_nodes.append(NLSetLightShadowAction)


class NLSetLightColorAction(NLActionNode):
    bl_idname = "NLSetLightColorAction"
    bl_label = "Set Light Color"
    bl_icon = 'COLOR'
    nl_category = "Lights"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLLightObjectSocket, "Light Object")
        self.add_input(NLColorSocket, "Color")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightColor"

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "color"
        ]


_nodes.append(NLSetLightColorAction)


class NLGetLightEnergy(NLParameterNode):
    bl_idname = "NLGetLightEnergy"
    bl_label = "Get Light Energy"
    nl_category = "Lights"
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLLightObjectSocket, "Light Object")
        self.add_output(NLParameterSocket, 'Enery')

    def get_output_names(self):
        return ['ENERGY']

    def get_netlogic_class_name(self):
        return "ULGetLightEnergy"

    def get_input_names(self):
        return ["lamp"]


_nodes.append(NLGetLightEnergy)


class NLGetLightColorAction(NLParameterNode):
    bl_idname = "NLGetLightColorAction"
    bl_label = "Get Light Color"
    nl_category = "Lights"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLLightObjectSocket, "Light Object")
        self.add_output(NLColorSocket, 'Color')

    def get_output_names(self):
        return ['COLOR']

    def get_netlogic_class_name(self):
        return "ULGetLightColor"

    def get_input_names(self):
        return ["lamp"]


_nodes.append(NLGetLightColorAction)


class NLActionPlayActionNode(NLActionNode):
    bl_idname = "NLActionPlayActionNode"
    bl_label = "Play Animation"
    nl_category = "Animation"
    nl_module = 'actions'

    advanced: BoolProperty(
        name='Advanced',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object / Armature")
        self.add_input(NodeSocketLogicAnimation, "Action")
        self.add_input(NLFloatFieldSocket, "Start")
        self.add_input(NLFloatFieldSocket, "End")
        self.add_input(NLPositiveIntegerFieldSocket, "Layer")
        self.add_input(NLPositiveIntegerFieldSocket, "Priority")
        self.inputs[-1].enabled = False
        self.add_input(NLPlayActionModeSocket, "Play Mode")
        self.add_input(NLBooleanSocket, "Stop When Done")
        self.inputs[-1].value = True
        self.inputs[-1].enabled = False
        self.add_input(NLSocketAlphaFloat, "Layer Weight")
        self.inputs[-1].value = 1.0
        self.inputs[-1].enabled = False
        self.add_input(NLPositiveFloatSocket, "Speed")
        self.inputs[-1].value = 1.0
        self.inputs[-1].enabled = False
        self.add_input(NLFloatFieldSocket, "Blendin")
        self.inputs[-1].enabled = False
        self.add_input(NLBlendActionModeSocket, "Blend Mode")
        self.inputs[-1].enabled = False
        self.add_output(NLConditionSocket, "Started")
        self.add_output(NLConditionSocket, "Running")
        self.add_output(NLConditionSocket, "On Finish")
        self.add_output(NLParameterSocket, "Current Frame")

    def update_draw(self):
        if len(self.inputs) < 12:
            return
        self.inputs[6].enabled = False
        if self.inputs[7].value == 'bge.logic.KX_ACTION_MODE_LOOP':
            self.inputs[8].enabled = False
        else:
            self.inputs[8].enabled = True
        adv = [8, 9, 10, 11, 12]
        for x in adv:
            self.inputs[x].enabled = self.advanced

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_netlogic_class_name(self):
        return "ULPlayAction"

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "start_frame",
            "end_frame",
            "layer",
            "priority",
            "play_mode",
            "stop",
            "layer_weight",
            "speed",
            "blendin",
            "blend_mode"
        ]

    def get_output_names(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]


_nodes.append(NLActionPlayActionNode)


class NLActionAlignAxisToVector(NLActionNode):
    bl_idname = "NLActionAlignAxisToVector"
    bl_label = "Align Axis to Vector"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Vector")
        self.add_input(NLSocketOrientedLocalAxis, "Axis")
        self.add_input(NLSocketAlphaFloat, "Factor")
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULAlignAxisToVector"

    def get_input_names(self):
        return ["condition", "game_object", "vector", "axis", 'factor']

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionAlignAxisToVector)


# If the condition stays true for N seconds, do something,
# then stay true
class NLActionTimeBarrier(NLConditionNode):
    bl_idname = 'NLActionTimeBarrier'
    bl_label = 'Barrier'
    nl_category = 'Time'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLTimeSocket, 'Time')
        self.add_output(NLConditionSocket, 'Out')

    def get_netlogic_class_name(self):
        return 'ULBarrier'

    def get_input_names(self):
        return ['condition', 'time']


_nodes.append(NLActionTimeBarrier)


class NLActionTimeDelay(NLActionNode):
    bl_idname = 'NLActionTimeDelay'
    bl_label = 'Delay'
    bl_icon = 'PREVIEW_RANGE'
    nl_category = 'Time'
    nl_module = 'conditions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, 'Condition')
        self.add_input(NLTimeSocket, 'Delay')
        self.add_output(NLConditionSocket, 'Out')

    def get_netlogic_class_name(self):
        return 'ULTimeDelay'

    def get_input_names(self):
        return ['condition', 'delay']


_nodes.append(NLActionTimeDelay)


# When the condition is True,
# set to True then do the next check only after
# N seconds have elapsed
class NLActionTimeFilter(NLConditionNode):
    bl_idname = "NLActionTimeFilter"
    bl_label = "Pulsify"
    bl_icon = 'TEMP'
    nl_category = "Time"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLTimeSocket, "Gap")
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, "Out")

    def get_netlogic_class_name(self):
        return "ULPulsify"

    def get_input_names(self):
        return ["condition", "delay"]


_nodes.append(NLActionTimeFilter)


class NLActionMouseLookNode(NLActionNode):
    bl_idname = "NLActionMouseLookNode"
    bl_label = "Mouse Look"
    bl_icon = 'CAMERA_DATA'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'actions'
    axis: EnumProperty(
        name='Axis',
        items=_enum_look_axis,
        update=update_draw,
        default="1"
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Main Object")
        self.add_input(NLGameObjectSocket, "Head (Optional)")
        self.add_input(NLInvertedXYSocket, "")
        self.add_input(NLFloatFieldSocket, "Sensitivity")
        self.inputs[-1].value = 1.0
        self.add_input(NLBooleanSocket, "Cap Left / Right")
        self.add_input(NLAngleLimitSocket, "")
        self.add_input(NLBooleanSocket, "Cap Up / Down")
        self.add_input(NLAngleLimitSocket, "")
        self.inputs[-1].value_x = math.radians(-89)
        self.inputs[-1].value_y = math.radians(89)
        self.add_input(NLSocketAlphaFloat, "Smoothing")
        self.add_output(NLConditionSocket, 'Done')
        self.update_draw()

    def draw_buttons(self, context, layout):
        r = layout.row(align=True)
        r.label(text="Front:")
        r.prop(self, "axis", text="")

    def update_draw(self):
        if len(self.inputs) < 10:
            return
        if self.inputs[5].value:
            self.inputs[6].enabled = True
        else:
            self.inputs[6].enabled = False
        if self.inputs[7].value:
            self.inputs[8].enabled = True
        else:
            self.inputs[8].enabled = False

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULMouseLook"

    def get_attributes(self):
        return [("axis", lambda: self.axis)]

    def get_input_names(self):
        return [
            "condition",
            "game_object_x",
            "game_object_y",
            "inverted",
            "sensitivity",
            "use_cap_z",
            "cap_z",
            "use_cap_y",
            "cap_y",
            'smooth'
        ]


_nodes.append(NLActionMouseLookNode)


class NLActionPrint(NLActionNode):
    bl_idname = "NLActionPrint"
    bl_label = "Print"
    bl_icon = 'CONSOLE'
    nl_category = "Utilities"
    nl_module = 'actions'

    msg_type: EnumProperty(items=_enum_msg_types, name='Type', description='The Message Type defines the color when using the on-screen console')

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_input(NLQuotedStringFieldSocket, "Value")
        self.add_output(NLConditionSocket, 'Done')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'msg_type', text='')

    def get_attributes(self):
        return [("msg_type", lambda: f'"{self.msg_type}"')]

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULPrintValue"

    def get_input_names(self):
        return ["condition", "value"]


_nodes.append(NLActionPrint)


class NLActionMousePickNode(NLActionNode):
    bl_idname = "NLActionMousePickNode"
    bl_label = "Mouse Ray"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Ray Casts"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Camera")
        self.add_input(NLQuotedStringFieldSocket, "Property")
        self.add_input(NLBooleanSocket, 'X-Ray')
        self.add_input(NLFloatFieldSocket, "Distance")
        self.inputs[-1].value = 100.0
        self.add_output(NLConditionSocket, "Has Result")
        self.add_output(NLGameObjectSocket, "Picked Object")
        self.add_output(NLVectorSocket, "Picked Point")
        self.add_output(NLVectorSocket, "Picked Normal")

    def get_netlogic_class_name(self):
        return "ULMouseRayCast"

    def get_input_names(self):
        return ["condition", "camera", "property", 'xray', "distance"]

    def get_output_names(self):
        return [utils.OUTCELL, "OUTOBJECT", "OUTPOINT", "OUTNORMAL"]


_nodes.append(NLActionMousePickNode)


class NLActionCameraPickNode(NLActionNode):
    bl_idname = "NLActionCameraPickNode"
    bl_label = "Camera Ray"
    bl_icon = 'CAMERA_DATA'
    nl_category = "Ray Casts"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Camera")
        self.add_input(NLVec2FieldSocket, "Aim")
        self.add_input(NLQuotedStringFieldSocket, "Property")
        self.add_input(NLBooleanSocket, 'X-Ray')
        self.add_input(NLFloatFieldSocket, "Distance")
        self.inputs[-1].value = 100.0
        self.add_output(NLConditionSocket, "Has Result")
        self.add_output(NLGameObjectSocket, "Picked Object")
        self.add_output(NLVectorSocket, "Picked Point")
        self.add_output(NLVectorSocket, "Picked Normal")

    def get_netlogic_class_name(self):
        return "ULCameraRayCast"

    def get_input_names(self):
        return ["condition", "camera", "aim", "property_name", "xray", "distance"]

    def get_output_names(self):
        return [utils.OUTCELL, "PICKED_OBJECT", "PICKED_POINT", "PICKED_NORMAL"]


_nodes.append(NLActionCameraPickNode)


class NLActionSetParentNode(NLActionNode):
    bl_idname = "NLActionSetParentNode"
    bl_label = "Set Parent"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Child Object")
        self.add_input(NLGameObjectSocket, "Parent Object")
        self.add_input(NLBooleanSocket, "Compound")
        self.inputs[-1].value = True
        self.inputs[-1].enabled = False
        self.add_input(NLBooleanSocket, "Ghost")
        self.inputs[-1].value = True
        self.inputs[-1].enabled = False
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetParent"

    def get_input_names(self):
        return [
            "condition",
            "child_object",
            "parent_object",
            "compound",
            "ghost"
        ]


_nodes.append(NLActionSetParentNode)


class NLActionRemoveParentNode(NLActionNode):
    bl_idname = "NLActionRemoveParentNode"
    bl_label = "Remove Parent"
    bl_icon = 'X'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Child Object")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRemoveParent"

    def get_input_names(self):
        return ["condition", "child_object"]


_nodes.append(NLActionRemoveParentNode)


class NLActionGetPerformanceProfileNode(NLActionNode):
    bl_idname = "NLActionGetPerformanceProfileNode"
    bl_label = "Get Profile"
    bl_icon = 'TEXT'
    nl_category = "Utilities"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_input(NLBooleanSocket, "Print Profile")
        self.add_input(NLBooleanSocket, "Evaluated Nodes")
        self.add_input(NLBooleanSocket, "Nodes per Second")
        self.add_input(NLBooleanSocket, "Nodes per Tick")
        self.add_output(NLConditionSocket, 'Done')
        self.add_output(NLParameterSocket, 'Profile')

    def get_output_names(self):
        return ["OUT", "DATA"]

    def get_netlogic_class_name(self):
        return "ULGetPerformanceProfile"

    def get_input_names(self):
        return [
            "condition",
            "print_profile",
            "check_evaluated_cells",
            'check_average_cells_per_sec',
            'check_cells_per_tick'
        ]


_nodes.append(NLActionGetPerformanceProfileNode)


class NLParameterGameObjectParent(NLParameterNode):
    bl_idname = "NLParameterGameObjectParent"
    bl_label = "Get Parent"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Child Object")
        self.add_output(NLGameObjectSocket, "Parent Object")

    def get_netlogic_class_name(self):
        return "ULGetParent"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterGameObjectParent)


class NLParameterAxisVector(NLParameterNode):
    bl_idname = "NLParameterAxisVector"
    bl_label = "Get Axis Vector"
    bl_icon = 'EMPTY_ARROWS'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'parameters'

    axis: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis,
        update=update_draw
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLVec3FieldSocket, "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'axis', text='')

    def get_netlogic_class_name(self):
        return "ULAxisVector"

    def get_input_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("axis", lambda: self.axis)]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterAxisVector)


class NLGetObjectDataName(NLParameterNode):
    bl_idname = "NLGetObjectDataName"
    bl_label = "Get Internal Name"
    bl_icon = 'FONT_DATA'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLParameterSocket, "Name")

    def get_netlogic_class_name(self):
        return "ULObjectDataName"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLGetObjectDataName)


class NLGetCurvePoints(NLParameterNode):
    bl_idname = "NLGetCurvePoints"
    bl_label = "Get Curve Points"
    bl_icon = 'OUTLINER_DATA_CURVE'
    nl_category = "Objects"
    nl_subcat = 'Curves'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLCurveObjectSocket, "Curve")
        self.add_output(NLListSocket, "Points")

    def get_netlogic_class_name(self):
        return "ULGetCurvePoints"

    def get_input_names(self):
        return ["curve"]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLGetCurvePoints)


class NLGetObjectVertices(NLParameterNode):
    bl_idname = "NLGetObjectVertices"
    bl_label = "Get Object Vertices"
    bl_icon = 'OUTLINER_DATA_MESH'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLGameObjectSocket, "Object")
        self.add_output(NLListSocket, "Vertices")

    def get_netlogic_class_name(self):
        return "ULObjectDataVertices"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLGetObjectVertices)


class NLSetBoneConstraintInfluence(NLActionNode):
    bl_idname = "NLSetBoneConstraintInfluence"
    bl_label = "Set Influence"
    bl_icon = 'CONSTRAINT_BONE'
    nl_category = "Animation"
    nl_subcat = 'Bone Constraints'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLArmatureObjectSocket, "Armature")
        self.add_input(NLArmatureBoneSocket, "")
        self.inputs[-1].ref_index = 1
        self.add_input(NLBoneConstraintSocket, "")
        self.inputs[-1].ref_index = 2
        self.add_input(NLSocketAlphaFloat, "Influence")
        self.add_output(NLConditionSocket, 'Done')

    # def update_draw(self):
    #     self.inputs[2].enabled = (
    #         self.inputs[1].value is not None or
    #         self.inputs[1].is_linked or
    #         self.inputs[1].use_owner
    #     )
    #     self.inputs[3].enabled = (
    #         self.inputs[2].enabled and
    #         (self.inputs[2].value != '' or
    #          self.inputs[2].is_linked)
    #     )

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintInfluence"

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "influence"
        ]


_nodes.append(NLSetBoneConstraintInfluence)


class NLSetBoneConstraintTarget(NLActionNode):
    bl_idname = "NLSetBoneConstraintTarget"
    bl_label = "Set Target"
    bl_icon = 'CONSTRAINT_BONE'
    nl_category = "Animation"
    nl_subcat = 'Bone Constraints'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLArmatureObjectSocket, "Armature")
        self.add_input(NLArmatureBoneSocket, "")
        self.inputs[-1].ref_index = 1
        self.add_input(NLBoneConstraintSocket, "")
        self.inputs[-1].ref_index = 2
        self.add_input(NLGameObjectSocket, "Target")
        self.add_output(NLConditionSocket, 'Done')

    # def update_draw(self):
    #     self.inputs[2].enabled = (
    #         self.inputs[1].value is not None or
    #         self.inputs[1].is_linked or
    #         self.inputs[1].use_owner
    #     )
    #     self.inputs[3].enabled = (
    #         self.inputs[2].enabled and
    #         (self.inputs[2].value != '' or
    #          self.inputs[2].is_linked)
    #     )

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintTarget"

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "target"
        ]


_nodes.append(NLSetBoneConstraintTarget)


class NLSetBoneConstraintAttribute(NLActionNode):
    bl_idname = "NLSetBoneConstraintAttribute"
    bl_label = "Set Attribute"
    bl_icon = 'CONSTRAINT_BONE'
    nl_category = "Animation"
    nl_subcat = 'Bone Constraints'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLArmatureObjectSocket, "Armature")
        self.add_input(NLArmatureBoneSocket, "")
        self.inputs[-1].ref_index = 1
        self.add_input(NLBoneConstraintSocket, "")
        self.inputs[-1].ref_index = 2
        self.add_input(NLQuotedStringFieldSocket, "Attribute")
        self.add_input(NLValueFieldSocket, "")
        self.add_output(NLConditionSocket, 'Done')

    # def update_draw(self):
    #     self.inputs[2].enabled = (
    #         self.inputs[1].value is not None or
    #         self.inputs[1].is_linked or
    #         self.inputs[1].use_owner
    #     )
    #     self.inputs[3].enabled = (
    #         self.inputs[2].enabled and
    #         (self.inputs[2].value != '' or
    #          self.inputs[2].is_linked)
    #     )

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintAttribute"

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "attribute",
            "value",
        ]


_nodes.append(NLSetBoneConstraintAttribute)


class NLActionSetBonePos(NLActionNode):
    bl_idname = "NLActionSetBonePos"
    bl_label = "Set Bone Position"
    bl_icon = 'BONE_DATA'
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLArmatureObjectSocket, "Armature")
        self.add_input(NLArmatureBoneSocket, "Bone Name")
        self.inputs[-1].ref_index = 1
        self.add_input(NLVec3FieldSocket, "Set Pos")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBonePosition"

    def get_input_names(self):
        return ["condition", "armature", "bone_name", "set_translation"]


_nodes.append(NLActionSetBonePos)


class NLActionEditBoneNode(NLActionNode):
    bl_idname = "NLActionEditBoneNode"
    bl_label = "Edit Bone"
    bl_icon = 'BONE_DATA'
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLArmatureObjectSocket, "Armature")
        self.add_input(NLArmatureBoneSocket, "Bone Name")
        self.inputs[-1].ref_index = 1
        self.add_input(NLVec3FieldSocket, "Set Pos")
        self.add_input(NLVec3FieldSocket, "Set Rot")
        self.add_input(NLVec3FieldSocket, "Set Scale")
        self.add_input(NLVec3FieldSocket, "Translate")
        self.add_input(NLVec3FieldSocket, "Rotate")
        self.add_input(NLVec3FieldSocket, "Scale")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULEditBone"

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone_name",
            "set_translation",
            "set_orientation",
            "set_scale",
            "translate",
            "rotate",
            "scale"
        ]


_nodes.append(NLActionEditBoneNode)


class NLActionSetDynamicsNode(NLActionNode):
    bl_idname = "NLActionSetDynamicsNode"
    bl_label = "Set Dynamics"
    bl_icon = 'FORCE_LENNARDJONES'
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, "Active")
        self.add_input(NLBooleanSocket, "Ghost")
        self.inputs[-1].value = False
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetDynamics"

    def get_input_names(self):
        return ["condition", "game_object", "activate", 'ghost']


_nodes.append(NLActionSetDynamicsNode)


class NLActionSetPhysicsNode(NLActionNode):
    bl_idname = "NLActionSetPhysicsNode"
    bl_label = "Set Physics"
    bl_icon = 'FORCE_LENNARDJONES'
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, "Active")
        self.add_input(NLBooleanSocket, "Cut Constraints")
        self.inputs[-1].value = False
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetPhysics"

    def get_input_names(self):
        return ["condition", "game_object", "activate", 'free_const']


_nodes.append(NLActionSetPhysicsNode)


class NLSetRigidBody(NLActionNode):
    bl_idname = "NLSetRigidBody"
    bl_label = "Set Rigid Body"
    bl_icon = 'FORCE_LENNARDJONES'
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, "Enabled")
        self.inputs[-1].value = True
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetRigidBody"

    def get_input_names(self):
        return ["condition", "game_object", "activate"]


_nodes.append(NLSetRigidBody)


class NLActionSetMousePosition(NLActionNode):
    bl_idname = "NLActionSetMousePosition"
    bl_label = "Set Position"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLFloatFieldSocket, "Screen X")
        self.inputs[-1].value = 0.5
        self.add_input(NLFloatFieldSocket, "Screen Y")
        self.inputs[-1].value = 0.5
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetMousePosition"

    def get_input_names(self):
        return ["condition", "screen_x", "screen_y"]


_nodes.append(NLActionSetMousePosition)


class NLActionSetMouseCursorVisibility(NLActionNode):
    bl_idname = "NLActionSetMouseCursorVisibility"
    bl_label = "Cursor Visibility"
    bl_icon = 'VIS_SEL_10'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLBooleanSocket, "Visible")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCursorVisibility"

    def get_input_names(self):
        return ["condition", "visibility_status"]


_nodes.append(NLActionSetMouseCursorVisibility)


class NLActionStart3DSoundAdv(NLActionNode):
    bl_idname = "NLActionStart3DSoundAdv"
    bl_label = "3D Sound"
    bl_icon = 'MUTE_IPO_ON'
    nl_category = "Sound"
    nl_module = 'actions'
    advanced: BoolProperty(
        name='Advanced Features',
        description='Show advanced features for this sound. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Speaker")
        self.add_input(NLSoundFileSocket, "Sound File")
        self.add_input(NLBooleanSocket, "Use Occlusion")
        self.add_input(NLSocketAlphaFloat, 'Transition')
        self.inputs[-1].value = .1
        self.add_input(NLSocketAlphaFloat, 'Lowpass')
        self.inputs[-1].value = .1
        self.add_input(NLSocketLoopCount, "Mode")
        self.add_input(NLPositiveFloatSocket, "Pitch")
        self.inputs[-1].value = 1.0
        self.add_input(NLPositiveFloatSocket, "Volume")
        self.inputs[-1].value = 1.0
        self.add_input(NLBooleanSocket, "Enable Reverb")
        self.add_input(NLPositiveFloatSocket, "Attenuation")
        self.inputs[-1].value = 1.0
        self.add_input(NLFloatFieldSocket, "Reference Distance")
        self.inputs[-1].format = True
        self.inputs[-1].value = 1.0
        self.add_input(NLVec2FieldSocket, "Cone Inner / Outer")
        self.inputs[-1].value_x = 360
        self.inputs[-1].value_y = 360
        self.add_input(NLFloatFieldSocket, "Cone Outer Volume")
        self.inputs[-1].format = True
        self.inputs[-1].value = 0.0
        self.add_input(NLBooleanSocket, "Ignore Timescale")
        self.add_output(NLConditionSocket, 'On Start')
        self.add_output(NLConditionSocket, 'On Finish')
        self.add_output(NLParameterSocket, 'Sound')

    def update_draw(self):
        self.inputs[4].enabled = self.inputs[5].enabled = self.inputs[3].value
        state = self.advanced
        for i in [9, 10, 11, 12, 13, 14]:
            ipt = self.inputs[i]
            if ipt.is_linked:
                ipt.enabled = True
            else:
                ipt.enabled = state

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSound3D"

    def get_input_names(self):
        return [
            "condition",
            "speaker",
            "sound",
            'occlusion',
            'transition',
            'cutoff',
            "loop_count",
            "pitch",
            "volume",
            'reverb',
            "attenuation",
            "distance_ref",
            "cone_angle",
            "cone_outer_volume",
            'ignore_timescale'
        ]


_nodes.append(NLActionStart3DSoundAdv)


class NLPlaySpeaker(NLActionNode):
    bl_idname = "NLPlaySpeaker"
    bl_label = "Start Speaker"
    bl_icon = 'MUTE_IPO_ON'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLSpeakerSocket, "Speaker")
        self.add_input(NLBooleanSocket, "Use Occlusion")
        self.add_input(NLSocketAlphaFloat, 'Transition')
        self.inputs[-1].value = .1
        self.add_input(NLSocketAlphaFloat, 'Lowpass')
        self.inputs[-1].value = .1
        self.add_input(NLSocketLoopCount, "Mode")
        self.add_input(NLBooleanSocket, "Ignore Timescale")
        self.add_output(NLConditionSocket, 'On Start')
        self.add_output(NLConditionSocket, 'On Finish')
        self.add_output(NLParameterSocket, 'Sound')

    def update_draw(self):
        self.inputs[3].enabled = self.inputs[4].enabled = self.inputs[2].value

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSpeaker"

    def get_input_names(self):
        return [
            "condition",
            "speaker",
            'occlusion',
            'transition',
            'cutoff',
            "loop_count",
            'ignore_timescale'
        ]


_nodes.append(NLPlaySpeaker)


class NLActionStartSound(NLActionNode):
    bl_idname = "NLActionStartSound"
    bl_label = "2D Sound"
    bl_icon = 'FILE_SOUND'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLSoundFileSocket, "Sound File")
        self.add_input(NLSocketLoopCount, "Mode")
        self.add_input(NLPositiveFloatSocket, "Pitch")
        self.inputs[-1].value = 1.0
        self.add_input(NLSocketAlphaFloat, "Volume")
        self.inputs[-1].value = 1.0
        self.add_input(NLBooleanSocket, "Ignore Timescale")
        self.add_output(NLConditionSocket, 'On Start')
        self.add_output(NLConditionSocket, 'On Finish')
        self.add_output(NLParameterSocket, 'Sound')

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSound"

    def get_input_names(self):
        return [
            "condition",
            "sound",
            "loop_count",
            "pitch",
            "volume",
            'ignore_timescale'
        ]


_nodes.append(NLActionStartSound)


class NLActionStopAllSounds(NLActionNode):
    bl_idname = "NLActionStopAllSounds"
    bl_label = "Stop All Sounds"
    bl_icon = 'CANCEL'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_output(NLConditionSocket, 'Done')

    def get_netlogic_class_name(self):
        return "ULStopAllSounds"

    def get_input_names(self):
        return ["condition"]


_nodes.append(NLActionStopAllSounds)


class NLActionStopSound(NLActionNode):
    bl_idname = "NLActionStopSound"
    bl_label = "Stop Sound"
    bl_icon = 'SNAP_FACE'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLParameterSocket, "Sound")
        self.add_output(NLConditionSocket, 'Done')

    def get_netlogic_class_name(self):
        return "ULStopSound"

    def get_input_names(self):
        return ["condition", "sound"]


_nodes.append(NLActionStopSound)


class NLActionPauseSound(NLActionNode):
    bl_idname = "NLActionPauseSound"
    bl_label = "Pause Sound"
    bl_icon = 'PAUSE'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLParameterSocket, "Sound")
        self.add_output(NLConditionSocket, 'Done')

    def get_netlogic_class_name(self):
        return "ULPauseSound"

    def get_input_names(self):
        return ["condition", "sound"]


_nodes.append(NLActionPauseSound)


class NLActionResumeSound(NLActionNode):
    bl_idname = "NLActionResumeSound"
    bl_label = "Resume Sound"
    bl_icon = 'FRAME_NEXT'
    nl_category = "Sound"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLParameterSocket, "Sound")
        self.add_output(NLConditionSocket, 'Done')

    def get_netlogic_class_name(self):
        return "ULResumeSound"

    def get_input_names(self):
        return ["condition", "sound"]


_nodes.append(NLActionResumeSound)


class NLActionEndGame(NLActionNode):
    bl_idname = "NLActionEndGame"
    bl_label = "Quit Game"
    bl_icon = 'SCREEN_BACK'
    nl_category = "Game"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")

    def get_netlogic_class_name(self):
        return "ULEndGame"

    def get_input_names(self):
        return ["condition"]


_nodes.append(NLActionEndGame)


class NLActionRestartGame(NLActionNode):
    bl_idname = "NLActionRestartGame"
    bl_label = "Restart Game"
    bl_icon = 'LOOP_BACK'
    nl_category = "Game"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRestartGame"

    def get_input_names(self):
        return ["condition"]


_nodes.append(NLActionRestartGame)


class NLActionStartGame(NLActionNode):
    bl_idname = "NLActionStartGame"
    bl_label = "Load File"
    nl_category = "Game"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLFilePathSocket, "File name")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULLoadBlendFile"

    def get_input_names(self):
        return ["condition", "file_name"]


_nodes.append(NLActionStartGame)


class NLParameterReceiveMessage(NLParameterNode):
    bl_idname = "NLParameterReceiveMessage"
    bl_label = "Receive"
    nl_category = "Events"
    nl_subcat = 'Custom'
    nl_module = 'conditions'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, "Subject")
        self.add_output(NLConditionSocket, "Received")
        self.add_output(NLParameterSocket, "Content")
        self.add_output(NLGameObjectSocket, "Messenger")

    def get_input_names(self):
        return ['subject']

    def get_output_names(self):
        return ["OUT", 'BODY', 'TARGET']

    def get_netlogic_class_name(self):
        return "ULHandleEvent"


_nodes.append(NLParameterReceiveMessage)


class NLParameterGetGlobalValue(NLParameterNode):
    bl_idname = "NLParameterGetGlobalValue"
    bl_label = "Get Global Value"
    nl_category = "Values"
    nl_subcat = 'Global'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLGlobalCatSocket, "Category")
        self.add_input(NLGlobalPropSocket, "Property")
        self.add_input(NLOptionalValueFieldSocket, "Default Value")
        self.add_output(NLParameterSocket, "Value")

    def get_input_names(self):
        return ["data_id", "key", 'default']

    def get_netlogic_class_name(self):
        return "ULGetGlobalValue"

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterGetGlobalValue)


class NLActionListGlobalValues(NLActionNode):
    bl_idname = "NLActionListGlobalValues"
    bl_label = "List Global Category"
    nl_category = "Values"
    nl_subcat = 'Global'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGlobalCatSocket, "Category")
        self.add_input(NLBooleanSocket, 'Print')
        self.add_output(NLConditionSocket, "Done")
        self.add_output(NLDictSocket, "Value")

    def get_input_names(self):
        return ['condition', "data_id", 'print_d']

    def get_output_names(self):
        return ["OUT", "VALUE"]

    def get_netlogic_class_name(self):
        return "ULListGlobalValues"


_nodes.append(NLActionListGlobalValues)


class NLActionCreateMessage(NLActionNode):
    bl_idname = "NLActionCreateMessage"
    bl_label = "Send"
    nl_category = "Events"
    nl_subcat = 'Custom'
    nl_module = 'actions'

    advanced: BoolProperty(
        name='Advanced',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLQuotedStringFieldSocket, "Subject")
        self.add_input(NLOptionalValueFieldSocket, "Content")
        self.add_input(NLGameObjectSocket, "Messenger")
        self.inputs[-1].use_owner = True
        self.add_output(NLConditionSocket, 'Done')

    def update_draw(self):
        adv = [2, 3]
        for x in adv:
            self.inputs[x].enabled = self.advanced

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "subject", "body", 'target']

    def get_netlogic_class_name(self):
        return "ULDispatchEvent"


_nodes.append(NLActionCreateMessage)


class NLActionSetGlobalValue(NLActionNode):
    bl_idname = "NLActionSetGlobalValue"
    bl_label = "Set Global Value"
    nl_category = "Values"
    nl_subcat = 'Global'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NodeSocketPseudoCondition, "Condition")
        self.add_input(NLGlobalCatSocket, "Category")
        self.add_input(NLGlobalPropSocket, "Property")
        self.inputs[-1].ref_index = 1
        self.add_input(NLValueFieldSocket, "")
        self.add_input(NLBooleanSocket, "Persistent")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "data_id", "key", "value", 'persistent']

    def get_netlogic_class_name(self):
        return "ULSetGlobalValue"


_nodes.append(NLActionSetGlobalValue)


class NLParameterFormattedString(NLParameterNode):
    bl_idname = "NLParameterFormattedString"
    bl_label = "Formatted String"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLQuotedStringFieldSocket, "Format String")
        self.inputs[-1].formatted = True
        self.inputs[-1].value = "A is {} and B is {}"
        self.add_input(NLQuotedStringFieldSocket, "A")
        self.inputs[-1].value = "Hello"
        self.add_input(NLQuotedStringFieldSocket, "B")
        self.inputs[-1].value = "World"
        self.add_input(NLQuotedStringFieldSocket, "C")
        self.add_input(NLQuotedStringFieldSocket, "D")
        self.add_output(NLParameterSocket, "String")

    def update_draw(self):
        string = self.inputs[0].value
        count = string.count('{}')
        ipts = [1, 2, 3, 4]
        for ipt in ipts:
            if ipt <= count:
                self.inputs[ipt].enabled = True
            else:
                self.inputs[ipt].enabled = False

    def get_input_names(self):
        return ["format_string", "value_a", "value_b", "value_c", "value_d"]

    def get_netlogic_class_name(self):
        return "ULFormattedString"

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterFormattedString)


class NLActionRandomInteger(NLActionNode):
    bl_idname = "NLActionRandomInteger"
    bl_label = "Random Integer"
    nl_category = "Values"
    nl_subcat = 'Random'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLIntegerFieldSocket, "Max")
        self.add_input(NLIntegerFieldSocket, "Min")
        self.add_output(NLParameterSocket, "Value")

    def get_input_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "ULRandomInt"

    def get_output_names(self):
        return ["OUT_A"]


_nodes.append(NLActionRandomInteger)


class NLActionRandomFloat(NLActionNode):
    bl_idname = "NLActionRandomFloat"
    bl_label = "Random Float"
    nl_category = "Values"
    nl_subcat = 'Random'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLFloatFieldSocket, "Max")
        self.add_input(NLFloatFieldSocket, "Min")
        self.add_output(NLParameterSocket, "Value")

    def get_input_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "ULRandomFloat"

    def get_output_names(self):
        return ["OUT_A"]


_nodes.append(NLActionRandomFloat)


class NLRandomVect(NLActionNode):
    bl_idname = "NLRandomVect"
    bl_label = "Random Vector"
    nl_category = "Values"
    nl_subcat = 'Random'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLXYZSocket, "")
        self.add_output(NLVectorSocket, "Vector")

    def get_input_names(self):
        return ['xyz']

    def get_netlogic_class_name(self):
        return "ULRandomVect"

    def get_output_names(self):
        return ["OUT_A"]


_nodes.append(NLRandomVect)


class NLParameterDistance(NLParameterNode):
    bl_idname = "NLParameterDistance"
    bl_label = "Distance"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLVec3FieldSocket, "A")
        self.add_input(NLVec3FieldSocket, "B")
        self.add_output(NLParameterSocket, "Distance")

    def get_input_names(self):
        return ["parama", "paramb"]

    def get_netlogic_class_name(self):
        return "ULDistance"

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterDistance)


class NLParameterKeyboardKeyCode(NLParameterNode):
    bl_idname = "NLParameterKeyboardKeyCode"
    bl_label = "Key Code"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'parameters'
    value: StringProperty(update=update_draw)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLKeyboardKeySocket, "")
        self.add_output(NLParameterSocket, "Code")

    def get_input_names(self):
        return ["key_code"]

    def get_netlogic_class_name(self):
        return "ULKeyCode"


_nodes.append(NLParameterKeyboardKeyCode)


class NLActionMoveTo(NLActionNode):
    bl_idname = "NLActionMoveTo"
    bl_label = "Move To"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Target Location")
        self.add_input(NLBooleanSocket, "Move as Dynamic")
        self.add_input(NLPositiveFloatSocket, "Speed")
        self.inputs[-1].value = 1.0
        self.add_input(NLFloatFieldSocket, "Stop At Distance")
        self.inputs[-1].value = 0.5
        self.add_output(NLConditionSocket, "When Done")

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "destination_point",
            'dynamic',
            "speed",
            "distance"
        ]

    def get_netlogic_class_name(self):
        return "ULMoveTo"


_nodes.append(NLActionMoveTo)


class NLActionTranslate(NLActionNode):
    bl_idname = "NLActionTranslate"
    bl_label = "Translate"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLBooleanSocket, "Local")
        self.add_input(NLVec3FieldSocket, "Vector")
        self.add_input(NLFloatFieldSocket, "Speed")
        self.inputs[-1].value = 1.0
        self.add_output(NLConditionSocket, "When Done")

    def get_input_names(self):
        return ["condition", "moving_object", "local", "vect", "speed"]

    def get_netlogic_class_name(self):
        return "ULTranslate"


_nodes.append(NLActionTranslate)


class NLActionRotateTo(NLActionNode):
    bl_idname = "NLActionRotateTo"
    bl_label = "Rotate To"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Object")
        self.add_input(NLVec3FieldSocket, "Target")
        self.add_input(NLSocketAlphaFloat, "Factor")
        self.inputs[-1].value = 1.0
        self.add_input(NLSocketLocalAxis, "Rot Axis")
        self.inputs[-1].value = '2'

        self.add_input(NLSocketOrientedLocalAxis, "Front")
        self.inputs[-1].value = '1'
        self.add_output(NLConditionSocket, "When Done")

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "target_point",
            "speed",
            "rot_axis",
            "front_axis"
        ]

    def get_netlogic_class_name(self):
        return "ULActionRotateTo"


_nodes.append(NLActionRotateTo)


class NLActionNavigate(NLActionNode):
    bl_idname = "NLActionNavigate"
    bl_label = "Move To with Navmesh"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Moving Object")
        self.add_input(NLGameObjectSocket, "Rotating Object")
        self.add_input(NLNavMeshSocket, "Navmesh Object")
        self.add_input(NLVec3FieldSocket, "Destination")
        self.add_input(NLBooleanSocket, "Move as Dynamic")
        self.add_input(NLPositiveFloatSocket, "Lin Speed")
        self.inputs[-1].value = 1.0
        self.add_input(NLPositiveFloatSocket, "Reach Threshold")
        self.inputs[-1].value = 1.0
        self.add_input(NLBooleanSocket, "Look At")
        self.inputs[-1].value = True
        self.add_input(NLSocketLocalAxis, "Rot Axis")
        self.add_input(NLSocketOrientedLocalAxis, "Front")
        self.add_input(NLFloatFieldSocket, "Rot Speed")
        self.inputs[-1].value = 1.0
        self.add_input(NLBooleanSocket, "Visualize")
        self.add_output(NLConditionSocket, "Done")
        self.add_output(NLConditionSocket, "When Reached")
        self.add_output(NLListSocket, "Next Point")

    def get_output_names(self):
        return ["OUT", "FINISHED", "POINT"]

    def get_netlogic_class_name(self):
        return "ULMoveToWithNavmesh"

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "rotating_object",
            "navmesh_object",
            "destination_point",
            "move_dynamic",
            "linear_speed",
            "reach_threshold",
            "look_at",
            "rot_axis",
            "front_axis",
            "rot_speed",
            'visualize'
        ]


_nodes.append(NLActionNavigate)


class NLActionFollowPath(NLActionNode):
    bl_idname = "NLActionFollowPath"
    bl_label = "Follow Path"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.add_input(NLConditionSocket, "Condition")
        self.add_input(NLGameObjectSocket, "Moving Object")
        self.add_input(NLGameObjectSocket, "Rotating Object")
        self.add_input(NLListSocket, "Path Points")
        self.add_input(NLBooleanSocket, "Loop")
        self.add_input(NLBooleanSocket, "Continue")
        self.add_input(NLNavMeshSocket, "Optional Navmesh")
        self.add_input(NLBooleanSocket, "Move as Dynamic")
        self.add_input(NLPositiveFloatSocket, "Lin Speed")
        self.inputs[-1].value = 1.0
        self.add_input(NLPositiveFloatSocket, "Reach Threshold")
        self.inputs[-1].value = .2
        self.add_input(NLBooleanSocket, "Look At")
        self.inputs[-1].value = True
        self.add_input(NLSocketAlphaFloat, "Rot Speed")
        self.inputs[-1].value = 1.0
        self.add_input(NLSocketLocalAxis, "Rot Axis")
        self.inputs[-1].value = "2"
        self.add_input(NLSocketOrientedLocalAxis, "Front")
        self.add_output(NLConditionSocket, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULFollowPath"

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "rotating_object",
            "path_points",
            "loop",
            "path_continue",
            "navmesh_object",
            "move_dynamic",
            "linear_speed",
            "reach_threshold",
            "look_at",
            "rot_speed",
            "rot_axis",
            "front_axis"
        ]


_nodes.append(NLActionFollowPath)


_enum_predefined_math_fun = [
    ("User Defined", "User Defined", "A formula defined by the user"),
    ("abs(a)", "abs(a)", "absolute value of a"),
    ("acos(a)", "acos(a)", "arc cosine of a, radians"),
    ("acosh(a)", "acosh(a)", "inverse hyperbolic cosine of a"),
    ("asin(a)", "asin(a)", "arc sine of a, radians"),
    ("asinh(a)", "asinh(a)", "inverse hyperbolic cosing of a"),
    ("atan(a)", "atan(a)", "arc tangent of a, radians"),
    ("atan2(a,b)", "atan2(a,b)", "atan(a / b), radians"),
    ("atanh(a)", "atanh(a)", "inverse hyperbolic tangent of a"),
    ("ceil(a)", "ceil(a)", "smallest integer value = or > to a"),
    ("cos(a)", "cos(a)", "cosine of a, radians"),
    ("cosh(a)", "cosh(a)", "hyperbolic cosine of a"),
    ("curt(a)", "curt(a)", "cubic root of a"),
    ("degrees(a)", "degrees(a)", "convert a from radians to degrees"),
    ("e", "e", "the e constant"),
    ("exp(a)", "exp(e)", "e to the power a"),
    ("floor(a)", "floor(a)", "largest integer value < or = to a"),
    ("hypot(a,b)", "hypot(a,b)", "sqrt(a*a + b*b)"),
    ("log(a)", "log(a)", "natural log of a"),
    ("log10(a)", "log10(a)", "base 10 log of a"),
    ("mod(a,b)", "mod(a,b)", "a modulo b"),
    ("pi", "pi", "the PI constant"),
    ("pow(a,b)", "pow(a,b)", "a to the power b"),
    ("radians(a)", "radians(a)", "convert a from degrees to radians"),
    ("sign(a)", "sign(a)", "0 if a is 0, -1 if a < 0, 1 if a > 0"),
    ("sin(a)", "sin(a)", "sine of a, radians"),
    ("sinh(a)", "sinh(a)", "hyperbolic sine of a"),
    ("sqrt(a)", "sqrt(a)", "square root of a"),
    ("tan(a)", "tan(a)", "tangent of a, radians"),
    ("tanh(a)", "tanh(a)", "hyperbolic tangent of a")
]


class NLParameterMathFun(NLParameterNode):
    bl_idname = "NLParameterMathFun"
    bl_label = "Formula"
    nl_category = "Math"
    nl_module = 'parameters'

    def on_fun_changed(self, context):
        if(self.predefined_formulas != "User Defined"):
            self.value = self.predefined_formulas
        update_tree_code(self, context)

    value: StringProperty(
        update=update_draw
    )
    predefined_formulas: EnumProperty(
        name='Operation',
        items=_enum_predefined_math_fun,
        update=on_fun_changed,
        default="User Defined")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.add_input(NLFloatFieldSocket, "a")
        self.add_input(NLFloatFieldSocket, "b")
        self.add_output(NLParameterSocket, "Result")
        self.value = "a + b"

    def draw_buttons(self, context, layout):
        layout.prop(self, "predefined_formulas", text="Predef.")
        if self.predefined_formulas == 'User Defined':
            layout.prop(self, "value", text="Formula")

    def get_input_names(self):
        return ["a", "b"]

    def get_attributes(self):
        return [("formula", '"{0}"'.format(self.value))]

    def get_netlogic_class_name(self):
        return "ULFormula"

    def get_output_names(self):
        return ["OUT"]


_nodes.append(NLParameterMathFun)
