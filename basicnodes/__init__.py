import math
import bpy
import bge_netlogic
from bge_netlogic import utilities as utils
from ui import LogicNodeTree
from utilities import make_valid_name
from bpy.props import StringProperty
from bpy.props import FloatProperty
from bpy.props import PointerProperty
from bpy.props import IntProperty
from bpy.props import IntVectorProperty
from bpy.props import FloatVectorProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import BoolVectorProperty
from bpy.props import CollectionProperty
import socket
import os


TOO_OLD = bpy.app.version < (2, 80, 0)

INVALID = 'INVALID'

CONDITION_SOCKET_COLOR = utils.Color.RGBA(0.8, 0.2, 0.2, 1.0)
PARAMETER_SOCKET_COLOR = utils.Color.RGBA(.631, .631, .631, 1.0)
PARAM_BOOL_SOCKET_COLOR = utils.Color.RGBA(.8, 0.651, .839, 1.0)
PARAM_INT_SOCKET_COLOR = utils.Color.RGBA(.349, 0.549, .361, 1.0)
PARAM_COLOR_SOCKET_COLOR = utils.Color.RGBA(.78, .78, .161, 1.0)
PARAM_LIST_SOCKET_COLOR = utils.Color.RGBA(0.74, .65, .48, 1.0)
PARAM_DICT_SOCKET_COLOR = utils.Color.RGBA(0.58, 0.48, .74, 1.0)
PARAM_OBJ_SOCKET_COLOR = utils.Color.RGBA(0.929, 0.620, .361, 1.0)
PARAM_MAT_SOCKET_COLOR = utils.Color.RGBA(.922, .459, .51, 1.0)
PARAM_GEOMTREE_SOCKET_COLOR = utils.Color.RGBA(.45, .8, .58, 1.0)
PARAM_TEXT_SOCKET_COLOR = utils.Color.RGBA(.388, .220, .388, 1.0)
PARAM_MESH_SOCKET_COLOR = utils.Color.RGBA(.0, .839, .639, 1.0)
PARAM_COLL_SOCKET_COLOR = utils.Color.RGBA(0.961, 0.961, .961, 1.0)
PARAM_SCENE_SOCKET_COLOR = utils.Color.RGBA(0.5, 0.5, 0.6, 1.0)
PARAM_VECTOR_SOCKET_COLOR = utils.Color.RGBA(0.388, 0.388, 0.78, 1.0)
PARAM_SOUND_SOCKET_COLOR = utils.Color.RGBA(.388, .220, .388, 1.0)
PARAM_IMAGE_SOCKET_COLOR = utils.Color.RGBA(.388, .220, .388, 1.0)
PARAM_LOGIC_BRICK_SOCKET_COLOR = utils.Color.RGBA(0.9, 0.9, 0.4, 1.0)
PARAM_PYTHON_SOCKET_COLOR = utils.Color.RGBA(0.2, 0.7, 1, 1.0)
ACTION_SOCKET_COLOR = utils.Color.RGBA(0.2, .7, .7, 1.0)

CONDITION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]

_sockets = []
_nodes = []


_enum_local_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "Z Axis", "The Local Z Axis [Integer Value 2]")
]

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


_enum_distance_models = [
    ('INVERSE', 'Inverse', 'Sound will fade exponentially (Realistic)'),
    ('INVERSE_CLAMPED', 'Inverse Clamped',
     'Sound will fade exponentially (Realistic, Clamped)'),
    ('EXPONENT', 'Exponent', 'Sound will fade detemined by an exponent (Good audibility)'),
    ('EXPONENT_CLAMPED', 'Exponent Clamped',
     'Sound will fade detemined by an exponent (Good audibility, Clamped)'),
    ('LINEAR', 'Linear', 'Sound will fade in a linear relation to distance'),
    ('LINEAR_CLAMPED', 'Linear Clamped',
     'Sound will fade in a linear relation to distance (Clamped)'),
    ('NONE', 'None', "Don't use a distance model")
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


_enum_ik_mode_values = [
    ("None", "None", "Not set"),
    (
        "bge.logic.CONSTRAINT_IK_MODE_INSIDE",
        "Inside",
        "Keep the bone with IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_OUTSIDE",
        "Outside",
        "Keep the bone outside IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_ONSURFACE",
        "On Surface",
        "Keep the bone exactly at IK Distance of the target"
    )
]


_enum_field_value_types = [
    ("STRING", "String", "A String"),
    ("FLOAT", "Float", "A Float value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("BOOLEAN", "Bool", "A True/False value"),
    ("FILE_PATH", "File Path", 'Choose a file path')
]

_enum_numeric_field_value_types = [
    ("NONE", "None", "The None value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("FLOAT", "Float", " A Float value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]

_enum_optional_float_value_types = [
    ("NONE", "None", "No value"),
    ("FLOAT", "Float", "A decimal value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]

_enum_vehicle_axis = [
    ("REAR", "Rear", "Apply to wheels without steering"),
    ("FRONT", "Front", "Apply to wheels with steering"),
    ("ALL", "All", "Apply to all wheels")
]


_enum_loop_count_values = [
    (
        "ONCE",
        "Play",
        (
            'Play once when condition is TRUE, then wait for '
            'the condition to become TRUE again to play it again.'
        )
    ), (
        "INFINITE",
        "Loop",
        "When condition is TRUE, start repeating the sound until stopped."
    ), (
        "CUSTOM",
        "Times",
        "When the condition it TRUE, play the sound N times"
    )
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

_enum_mouse_buttons = [
    ("bge.events.LEFTMOUSE", "Left Button", "Left Mouse Button"),
    ("bge.events.MIDDLEMOUSE", "Middle Button", "Middle Mouse Button"),
    ("bge.events.RIGHTMOUSE", "Right Button", "Right Mouse Button")
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

_enum_quality_levels = [
    ("LOW", "Low", "Set a lower quality to increase performance"),
    ("MEDIUM", "Medium", "Set a medium quality for a balanced performance"),
    ("HIGH", "High", "Set a high quality at the cost of performance"),
    ("ULTRA", "Ultra", "Set a very high quality at the cost of performance")
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


_enum_distance_checks = [
    ("0", "AB = Dist", "AB Distance equal to Dist [Integer value 0]"),
    ("1", "AB != Dist", "AB Distance not equal to Dist [Integer value 1]"),
    ("2", "AB > Dist", "AB Distance greater than Dist [Integer value 2]"),
    ("3", "AB < Dist", "AB Distance less than Dist [Integer value 3]"),
    (
        "4",
        "AB >= Dist",
        "AB Distance greater than or equal to Dist [Integer value 4]"
    ),
    (
        "5",
        "AB <= Dist",
        "AB Distance less than or equal to Dist [Integer value 5]"
    ),
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

_enum_blend_mode_values = [
    (
        "bge.logic.KX_ACTION_BLEND_BLEND",
        "Blend",
        "Blend layers using linear interpolation"
    ),
    ("bge.logic.KX_ACTION_BLEND_ADD", "Add", "Adds the layer together")
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


OUTCELL = "__standard_logic_cell_value__"


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
    utils.set_compile_status(utils.TREE_MODIFIED)
    if utils.is_compile_status(utils.TREE_COMPILED_ALL):
        return
    if not hasattr(context.space_data, 'edit_tree'):
        return
    tree = context.space_data.edit_tree
    if not tree:
        return
    for node in tree.nodes:
        if isinstance(node, NLNode):
            try:
                node.update_draw()
            except Exception:
                pass
    if not getattr(bpy.context.scene.logic_node_settings, 'auto_compile'):
        return
    bge_netlogic.update_current_tree_code()


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
    nl_color: list = PARAMETER_SOCKET_COLOR
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
                self.mute = False
            except Exception as e:
                utils.error(
                    f'Error occured when writing sockets for {self.__class__} Node: {e}\n'
                    f'\tInfo:\n'
                    f'\tSocket: {socket}\n'
                    f'\tCellname: {cell_varname}\n'
                    f'\tNode: {self.label if self.label else self.name}\n'
                    '---END ERROR'
                )
                self.mute = True
        return text

    def write_socket_field_initialization(
        self,
        socket,
        cell_varname,
        uids
    ):
        text = ''
        input_names = self.get_input_sockets_field_names()
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

    def get_input_sockets_field_names(self):
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

        if not isinstance(output_node, NLNode):
            raise Exception('No NLNode')
        output_node_varname = uids.get_varname_for_node(output_node)
        output_map = output_node.get_output_socket_varnames()

        if output_map:
            varname = output_map[output_socket_index]
            if varname is OUTCELL:
                return output_node_varname
            else:
                return '{}.{}'.format(output_node_varname, varname)
        else:
            return output_node_varname

    def get_output_socket_varnames(self):
        return None

    def update(self):
        # bge_netlogic.update_current_tree_code()
        pass


class NLConditionSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLConditionSocket"
    bl_label = "Condition"
    description = StringProperty(default='Execution Condition')
    default_value: StringProperty(
        name='Condition',
        default="None"
    )
    type: StringProperty(default='MATERIAL')
    shape: StringProperty(default='CIRCLE')
    nl_color = CONDITION_SOCKET_COLOR

    # def draw_color(self, context, node):
    #     return CONDITION_SOCKET_COLOR

    def shape_setup(self):
        self.display_shape = self.shape

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return self.default_value


_sockets.append(NLConditionSocket)


class NodeSocketPseudoCondition(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPseudoConditionSocket"
    bl_label = "Condition"
    value: BoolProperty(
        name='Condition',
        description=(
            'Optional; When True, '
            'perform with each frame, when False, never perform'
        ),
        update=update_tree_code)
    type: StringProperty(default='MATERIAL')
    nl_color = CONDITION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            layout.prop(self, "value", text=label)

    def get_unlinked_value(self):
        return "True" if self.value else "False"


_sockets.append(NodeSocketPseudoCondition)


class NLParameterSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"
    type: StringProperty(default='VALUE')
    nl_color = PARAMETER_SOCKET_COLOR

    def draw_color(self, context, node):
        return self.nl_color

    def validate(self, link, from_socket):
        self.nl_color = from_socket.nl_color

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLParameterSocket)


class NLDictSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLDictSocket"
    bl_label = "Parameter"
    type: StringProperty(default='MATERIAL')

    def draw_color(self, context, node):
        return PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLDictSocket)


class NLUISocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLUISocket"
    bl_label = "Parameter"
    type: StringProperty(default='GEOMETRY')
    nl_color = PARAM_MESH_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLUISocket)


class NLListSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLListSocket"
    bl_label = "Parameter"
    # type: StringProperty(default='SQUARE')
    type: StringProperty(default='RGBA')
    nl_color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLListSocket)


class NLListItemSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLListItemSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        row = layout.row(align=True)
        row.label(text=text)
        row.operator(bge_netlogic.ops.NLRemoveListItemSocket.bl_idname, icon='X', text='')

    def get_unlinked_value(self):
        return None


_sockets.append(NLListItemSocket)


class NLCollisionMaskSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCollisionMaskSocket"
    bl_label = "Parameter"
    slot_0: BoolProperty(default=True)
    slot_1: BoolProperty(default=True)
    slot_2: BoolProperty(default=True)
    slot_3: BoolProperty(default=True)
    slot_4: BoolProperty(default=True)
    slot_5: BoolProperty(default=True)
    slot_6: BoolProperty(default=True)
    slot_7: BoolProperty(default=True)
    slot_8: BoolProperty(default=True)
    slot_9: BoolProperty(default=True)
    slot_10: BoolProperty(default=True)
    slot_11: BoolProperty(default=True)
    slot_12: BoolProperty(default=True)
    slot_13: BoolProperty(default=True)
    slot_14: BoolProperty(default=True)
    slot_15: BoolProperty(default=True)

    def draw_color(self, context, node):
        return PARAM_LIST_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column(align=True)
            col.scale_y = .8
            row = col.row(align=True)
            row2 = col.row(align=True)
            idx = 0
            while idx < 8:
                row.prop(self, f'slot_{idx}', text='',
                         emboss=True, icon='BLANK1')
                idx += 1
            while idx < 16:
                row2.prop(self, f'slot_{idx}', text='',
                          emboss=True, icon='BLANK1')
                idx += 1

    def get_unlinked_value(self):
        slots = [self.get(f'slot_{idx}', 1) * (2**idx) for idx in range(16)]
        return sum(slots)


_sockets.append(NLCollisionMaskSocket)


class NLLogicBrickSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLLogicBrickSocket"
    bl_label = "Property"
    value: StringProperty(
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit',
        update=update_tree_code
    )
    brick_type: StringProperty(default='controllers')

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            game_object = None
            game_obj_socket = self.node.inputs[self.ref_index]
            if not game_obj_socket.use_owner:
                game_object = game_obj_socket.value
            else:
                for obj in bpy.data.objects:
                    if f'{utils.NLPREFIX}{tree.name}' in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
                if not game_obj_socket.is_linked and game_object:
                    row.prop(self, 'use_custom', text='', icon='GREASEPENCIL')
            if game_object or game_obj_socket.is_linked:
                if not game_obj_socket.is_linked and not self.use_custom:
                    game = game_object.game
                    col.prop_search(
                        self,
                        'value',
                        game,
                        self.brick_type,
                        icon='NONE',
                        text=''
                    )
                else:
                    col.prop(self, 'value', text='')
            else:
                col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLLogicBrickSocket)


class NLPythonSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPythonSocket"
    bl_label = "Python"

    def draw_color(self, context, node):
        return PARAM_PYTHON_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLPythonSocket)


class NLActionSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLActionSocket"
    bl_label = "Action"

    def draw_color(self, context, node):
        return ACTION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)


_sockets.append(NLActionSocket)


class NLAbstractNode(NLNode):
    bl_icon = 'DOT'
    nl_separate = False
    search_tags = []

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

    def insert_link(self, link):
        to_socket = link.to_socket
        from_socket = link.from_socket
        try:
            to_socket.validate(link, from_socket)
        except Exception as e:
            utils.error(e)
            utils.debug(
                'Receiving Node not a Logic Node Type, skipping validation.'
            )

    def add_input(self, cls, name, socket_id):
        self.inputs.new(cls.bl_idname, name)
        self.inputs[-1].socket_id = socket_id

    def free(self):
        pass

    def draw_buttons(self, context, layout):
        pass

    def update_draw(self):
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def update(self):
        update_tree_code(self, bpy.context)

    # def draw_label(self):
    #    return self.__class__.bl_label


###############################################################################
# Basic Nodes
###############################################################################


class NLConditionNode(bpy.types.Node, NLAbstractNode):

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

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

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

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

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

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
    bl_label = "Object"
    value: PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        update=update_tree_code,
        description='Use the owner of this tree'
    )
    color = PARAM_OBJ_SOCKET_COLOR

    def draw_color(self, context, node):
        return self.color

    def is_scene_logic(self):
        return self.node.tree is bpy.context.scene.get('custom_mainloop_tree', None)

    def draw(self, context, layout, node, text):
        scene_logic = self.is_scene_logic()
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner or scene_logic:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                if not scene_logic:
                    row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.use_owner and not self.is_scene_logic():
            return '"NLO:U_O"'
        if isinstance(self.value, bpy.types.Object):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLGameObjectSocket)


class NLCameraSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCameraSocket"
    bl_label = "Camera"
    value: PointerProperty(
        name='Object',
        type=bpy.types.Object,
        poll=filter_camera,
        update=update_tree_code
    )
    use_active: BoolProperty(
        name='Use Active',
        update=update_tree_code,
        description='Use current active camera'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_active:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_active', icon='CAMERA_DATA', text='')

    def get_unlinked_value(self):
        if self.use_active:
            return 'self.owner.scene.active_camera'
        if isinstance(self.value, bpy.types.Object):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLCameraSocket)


class NLSpeakerSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSpeakerSocket"
    bl_label = "Camera"
    value: PointerProperty(
        name='Object',
        type=bpy.types.Object,
        poll=filter_speaker,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            row = col.row()
            if self.name:
                row.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.context.scene,
                'objects',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Object):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLSpeakerSocket)


class NLNavMeshSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNavMeshSocket"
    bl_label = "Object"
    value: PointerProperty(
        name='Object',
        type=bpy.types.Object,
        poll=filter_navmesh,
        update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        update=update_tree_code,
        description='Use the owner of this tree'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.use_owner:
            return '"NLO:U_O"'
        if isinstance(self.value, bpy.types.Object):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLNavMeshSocket)


class NLLightObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLLightObjectSocket"
    bl_label = "Light"
    value: PointerProperty(
        name='Light',
        type=bpy.types.Light,
        poll=filter_lights,
        update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        update=update_tree_code,
        description='Use the owner of this tree'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.use_owner:
            return '"NLO:U_O"'
        if isinstance(self.value, bpy.types.Light):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLLightObjectSocket)


class NLArmatureObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLArmatureObjectSocket"
    bl_label = "Armature"
    value: PointerProperty(
        name='Armature',
        type=bpy.types.Armature,
        poll=filter_armatures,
        update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        update=update_tree_code,
        description='Use the owner of this tree'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.use_owner:
            return '"NLO:U_O"'
        if isinstance(self.value, bpy.types.Object):
            return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLArmatureObjectSocket)


class NLCurveObjectSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCurveObjectSocket"
    bl_label = "Curve"
    value: PointerProperty(
        name='Armature',
        type=bpy.types.Curve,
        poll=filter_curves,
        update=update_tree_code
    )
    use_owner: BoolProperty(
        name='Use Owner',
        update=update_tree_code,
        description='Use the owner of this tree'
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            if not self.use_owner:
                col = layout.column(align=False)
                row = col.row()
                if self.name:
                    row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')
                col.prop_search(
                    self,
                    'value',
                    bpy.context.scene,
                    'objects',
                    icon='NONE',
                    text=''
                )
            else:
                row = layout.row()
                row.label(text=self.name)
                row.prop(self, 'use_owner', icon='USER', text='')

    def get_unlinked_value(self):
        if self.value is None:
            return "None"
        if self.use_owner:
            return '"NLO:U_O"'
        return '"NLO:{}"'.format(self.value.name)


_sockets.append(NLCurveObjectSocket)


class NLGamePropertySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGamePropertySocket"
    bl_label = "Property"
    value: StringProperty(
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        mode = getattr(self.node, 'mode', 'GAME')
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            game_object = None
            game_obj_socket = self.node.inputs[self.ref_index]
            if not game_obj_socket.use_owner:
                game_object = game_obj_socket.value
            else:
                prop_name = f'{utils.NLPREFIX}{make_valid_name(tree.name)}'
                for obj in bpy.data.objects:
                    if prop_name in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
                if not game_obj_socket.is_linked and game_object and mode == 'GAME':
                    row.prop(self, 'use_custom', text='', icon='GREASEPENCIL')
            if game_object or game_obj_socket.is_linked:
                if not game_obj_socket.is_linked and not self.use_custom and mode == 'GAME':
                    game = game_object.game
                    col.prop_search(
                        self,
                        'value',
                        game,
                        'properties',
                        icon='NONE',
                        text=''
                    )
                else:
                    col.prop(self, 'value', text='')
            else:
                col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLGamePropertySocket)


class NLArmatureBoneSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLArmatureBoneSocket"
    bl_label = "Property"
    value: StringProperty(
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            game_object = None
            game_obj_socket = self.node.inputs[self.ref_index]
            if not game_obj_socket.use_owner:
                game_object = game_obj_socket.value
            else:
                for obj in bpy.data.objects:
                    if f'{utils.NLPREFIX}{tree.name}' in obj.game.properties:
                        game_object = obj
                        break
            if self.name:
                row = col.row()
                row.label(text=self.name)
            if game_object and isinstance(game_object.data, bpy.types.Armature):
                if not game_obj_socket.is_linked:
                    col.prop_search(
                        self,
                        'value',
                        game_object.pose,
                        'bones',
                        icon='NONE',
                        text=''
                    )
                    return
            col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLArmatureBoneSocket)


class NLBoneConstraintSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBoneConstraintSocket"
    bl_label = "Property"
    value: StringProperty(
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            bone = None
            bone_socket = self.node.inputs[self.ref_index]
            armature_socket = self.node.inputs[bone_socket.ref_index]
            if not armature_socket.is_linked and not armature_socket.use_owner:
                armature = armature_socket.value
                bone = armature.pose.bones[bone_socket.value]
            if self.name:
                row = col.row()
                row.label(text=self.name)
            if bone and not armature_socket.use_owner:
                if not bone_socket.is_linked and not armature_socket.is_linked:
                    col.prop_search(
                        self,
                        'value',
                        bone,
                        'constraints',
                        text=''
                    )
                    return
            else:
                col.prop(self, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLBoneConstraintSocket)


class NLGeomNodeTreeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGeomNodeTreeSocket"
    bl_label = "Material"
    value: PointerProperty(
        name='Geometry Node Tree',
        type=bpy.types.GeometryNodeTree,
        poll=filter_geometry_nodes,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_GEOMTREE_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'node_groups',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.GeometryNodeTree):
            return '"{}"'.format(self.value.name)


_sockets.append(NLGeomNodeTreeSocket)


class NLNodeGroupSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNodeGroupSocket"
    bl_label = "Node Tree"
    value: PointerProperty(
        name='Node Tree',
        type=bpy.types.NodeTree,
        poll=filter_node_groups,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_SCENE_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'node_groups',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.NodeTree):
            return '"{}"'.format(self.value.name)


_sockets.append(NLNodeGroupSocket)


class NLNodeGroupNodeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNodeGroupNodeSocket"
    bl_label = "Tree Node"
    value: StringProperty(
        name='Tree Node',
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            tree_socket = self.node.inputs[self.ref_index]
            tree = tree_socket.value
            col = layout.column(align=False)
            if tree and not tree_socket.is_linked:
                col.prop_search(
                    self,
                    "value",
                    bpy.data.node_groups[tree.name],
                    'nodes',
                    text=''
                )
            elif tree_socket.is_linked:
                col.label(text=text)
                col.prop(self, 'value', text='')
            else:
                col.label(text=self.name)

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLNodeGroupNodeSocket)


class NLMaterialSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMaterialSocket"
    bl_label = "Material"
    value: PointerProperty(
        name='Material',
        type=bpy.types.Material,
        poll=filter_materials,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_MAT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'materials',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Material):
            return '"{}"'.format(self.value.name)


_sockets.append(NLMaterialSocket)


class NLTreeNodeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTreeNodeSocket"
    bl_label = "Tree Node"
    value: StringProperty(
        name='Tree Node',
        update=update_tree_code
    )
    ref_index: IntProperty(default=0)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            mat_socket = self.node.inputs[self.ref_index]
            mat = mat_socket.value
            col = layout.column(align=False)
            if mat and not mat_socket.is_linked:
                col.prop_search(
                    self,
                    "value",
                    bpy.data.materials[mat.name].node_tree,
                    'nodes',
                    text=''
                )
            elif mat_socket.is_linked:
                col.label(text=text)
                col.prop(self, 'value', text='')
            else:
                col.label(text=self.name)

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLTreeNodeSocket)


class NLSceneSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSceneSocket"
    bl_label = "Scene"
    value: PointerProperty(
        name='Scene',
        type=bpy.types.Scene,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_MAT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if self.name and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'scenes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Scene):
            return '"{}"'.format(self.value.name)


_sockets.append(NLSceneSocket)


class NLTextIDSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTextIDSocket"
    bl_label = "Text"
    value: PointerProperty(
        name='Text',
        type=bpy.types.Text,
        poll=filter_texts,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_TEXT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'texts',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Text):
            return '"{}"'.format(self.value.name.split('.')[0])


_sockets.append(NLTextIDSocket)


class NLMeshSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMeshSocket"
    bl_label = "Mesh"
    value: PointerProperty(
        name='Mesh',
        type=bpy.types.Mesh,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_MESH_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'meshes',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Mesh):
            return '"{}"'.format(self.value.name)


_sockets.append(NLMeshSocket)


class NLGameObjectNameSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGameObjectNameSocket"
    bl_label = "Object"
    value: PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_OBJ_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text:
                col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.context.scene,
                'objects',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Object):
            return '"{}"'.format(self.value.name)


_sockets.append(NLGameObjectNameSocket)


class NLCollectionSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCollectionSocket"
    bl_label = "Collection"
    value: PointerProperty(
        name='Collection',
        type=bpy.types.Collection,
        description=(
            'Select a Collection. '
            'Objects in that collection will be used for the node'
        ),
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_COLL_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=text)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'collections',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Collection):
            return '"{}"'.format(self.value.name)


_sockets.append(NLCollectionSocket)


class NLSocketLogicTree(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLogicTree"
    bl_label = "Logic Tree"
    value: PointerProperty(
        name='Logic Tree',
        type=bpy.types.NodeTree,
        description=(
            'Select a Logic Tree'
        ),
        poll=filter_logic_trees,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        icon = 'OUTLINER' if not TOO_OLD else 'PLUS'
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column(align=False)
            if text and self.is_linked:
                col.label(text=text)
            col.prop_search(
                self,
                "value",
                bpy.data,
                'node_groups',
                icon=icon,
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.NodeTree):
            return '"{}"'.format(self.value.name)


_sockets.append(NLSocketLogicTree)


class NLAnimationSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLAnimationSocket"
    bl_label = "Action"
    value: PointerProperty(
        name='Action',
        type=bpy.types.Action,
        description='Select an Action',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text and self.is_linked:
                col.label(text=text)
            col.prop_search(
                self,
                "value",
                bpy.data,
                'actions',
                icon='ACTION',
                text=''
            )

    def get_unlinked_value(self):
        if isinstance(self.value, bpy.types.Action):
            return '"{}"'.format(self.value.name)


_sockets.append(NLAnimationSocket)


class NLSoundFileSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSoundFileSocket"
    bl_label = "String"
    filepath_value: StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code
    )
    sound_value: PointerProperty(
        name='Sound',
        type=bpy.types.Sound,
        description='Select a Sound',
        update=update_tree_code
    )
    use_path: BoolProperty(
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_SOUND_SOCKET_COLOR

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
                bge_netlogic.ops.NLLoadSoundOperator.bl_idname, icon='FILEBROWSER', text='')

    def get_unlinked_value(self):
        if not self.use_path and self.sound_value is None:
            return '"None"'
        path = str(self.filepath_value) if self.use_path else str(
            self.sound_value.filepath)
        path = path.replace('\\', '/')
        if path.endswith('\\'):
            path = path[:-1]
        return '"{}"'.format(path)


_sockets.append(NLSoundFileSocket)


class NLImageSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLImageSocket"
    bl_label = "Image"
    value: PointerProperty(
        name='Image',
        type=bpy.types.Image,
        description='Select an Image',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_IMAGE_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                row = col.row(align=True)
                row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "value", text='')
            row2.operator(
                bge_netlogic.ops.NLLoadImageOperator.bl_idname, icon='FILEBROWSER', text='')

    def get_unlinked_value(self):
        if self.value is None:
            return '"None"'
        return '"{}"'.format(str(self.value.name))


_sockets.append(NLImageSocket)


class NLFontSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFontSocket"
    bl_label = "Font"
    value: PointerProperty(
        name='Font',
        type=bpy.types.VectorFont,
        description='Select a Font',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_IMAGE_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                row = col.row(align=True)
                row.label(text=text)
            row2 = col.row(align=True)
            row2.prop(self, "value", text='')
            row2.operator(
                bge_netlogic.ops.NLLoadFontOperator.bl_idname, icon='FILEBROWSER', text='')

    def get_unlinked_value(self):
        if self.value is None:
            return '""'
        return '"{}"'.format(str(self.value.name))
        # path = self.value.filepath.replace('\\', '/')
        # return '"{}"'.format(os.path.join(path))


_sockets.append(NLFontSocket)


###############################################################################
# String Pointer Sockets
###############################################################################


class NLGlobalCatSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGlobalCatSocket"
    bl_label = "Category"
    value: StringProperty(
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            col.prop_search(
                self,
                "value",
                context.scene,
                'nl_global_categories',
                icon='OUTLINER_COLLECTION',
                text=''
            )

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLGlobalCatSocket)


class NLGlobalPropSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLGlobalPropSocket"
    bl_label = "Category"
    value: StringProperty(
        update=update_tree_code
    )
    ref_index: IntProperty(
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            ref_socket = self.node.inputs[self.ref_index]
            if ref_socket.is_linked:
                col.prop(self, 'value', text='')
            else:
                cat = context.scene.nl_global_categories[ref_socket.value]
                col.prop_search(
                    self,
                    "value",
                    cat,
                    'content',
                    icon='DOT',
                    text=''
                )

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLGlobalPropSocket)


###############################################################################
# Value Sockets
###############################################################################

# Mixin for Vector-Sockets
class _NLSocket_Vec3(NLSocket):
    bl_label = "Float Value"
    nl_color = PARAM_VECTOR_SOCKET_COLOR # gets picked up by NLSocket.draw_color
    type: StringProperty(default='VECTOR') # doesn't seem to be used ?
    # PyProps into Vector instead of the original individual BPyProps
    value_x= property(lambda s:s.value[0], lambda s,v:s.value.__setitem__(0, v))
    value_y= property(lambda s:s.value[1], lambda s,v:s.value.__setitem__(1, v))
    value_z= property(lambda s:s.value[2], lambda s,v:s.value.__setitem__(2, v))

    def get_unlinked_value(self):  # no longer individual calls
        return f"mathutils.Vector({tuple(self.value)})"

    def draw(self, context, layout, node, text):
        layout = layout.column(align=True)
        if text:
            layout.label(text=text)
        if not self.is_linked or self.is_output:
            if self.node.width >= 200:
                layout = layout.row(align=True)
            layout.prop(self, "value", text="")


class NLSocketAlphaFloat(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketAlphaFloat"
    bl_label = "Factor"
    value: FloatProperty(
        name='Alpha Value',
        description='Value range from 0 - 1',
        min=0.0,
        max=1.0,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", slider=True, text=text)
        pass

    def get_unlinked_value(self):
        return "{}".format(self.value)


_sockets.append(NLSocketAlphaFloat)


class NLSocketLogicOperator(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLogicOperator"
    bl_label = "Logic Operator"
    value: EnumProperty(
        name='Operation',
        items=_enum_logic_operators,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        self.value.replace('\\', '\\\\')
        return "{}".format(self.value)


_sockets.append(NLSocketLogicOperator)


class NLSocketControllerButtons(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketControllerButtons"
    bl_label = "Controller Buttons"
    value: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return "{}".format(self.value)


_sockets.append(NLSocketControllerButtons)


class NLQualitySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLQualitySocket"
    bl_label = "Quality"
    value: EnumProperty(
        name='Quality',
        items=_enum_quality_levels,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            if text:
                col = layout.column()
                col.label(text=text)
                col.prop(self, 'value', text='')
            else:
                layout.prop(self, "value", text='')

    def get_unlinked_value(self):
        return "'{}'".format(self.value)


_sockets.append(NLQualitySocket)


class NLSocketDistanceCheck(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketDistanceCheck"
    bl_label = "Distance Operator"
    value: EnumProperty(
        name='Mode',
        items=_enum_distance_checks,
        update=update_tree_code
    )
    def draw_color(self, context, node): return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return "{}".format(self.value)


_sockets.append(NLSocketDistanceCheck)


class NLSocketLoopCount(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLoopCount"
    bl_label = "Loop Count"
    value: StringProperty(update=update_tree_code)

    def update_value(self, context):
        current_type = self.value_type
        if current_type == "INFINITE":
            self.value = "-1"
        elif current_type == "ONCE":
            self.value = "1"
        elif current_type == "CUSTOM":
            self.value = '{}'.format(int(self.integer_editor) - 1)
    value_type: EnumProperty(
        name='Loop Count',
        items=_enum_loop_count_values,
        update=update_value
    )
    integer_editor: IntProperty(
        update=update_value,
        min=1,
        default=1,
        description=(
            'How many times the sound should '
            'be repeated when the condition is TRUE'
        )
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            current_type = self.value_type
            if (current_type == "INFINITE") or (current_type == "ONCE"):
                layout.label(text=text)
                layout.prop(self, "value_type", text="")
            else:
                layout.prop(self, "integer_editor", text="")
                layout.prop(self, "value_type", text="")

    def get_unlinked_value(self):
        current_type = self.value_type
        if current_type == "INFINITE":
            return "-1"
        if current_type == "ONCE":
            return "0"
        return '{}'.format(self.value)


_sockets.append(NLSocketLoopCount)


class NLBooleanSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBooleanSocket"
    bl_label = "Boolean"
    value: BoolProperty(update=update_tree_code)
    use_toggle: BoolProperty(default=False)
    true_label: StringProperty()
    false_label: StringProperty()
    type: StringProperty(default='STRING')

    def draw_color(self, context, node):
        return PARAM_BOOL_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            status = self.value
            if self.use_toggle:
                if status:
                    label = '{}: ON'.format(text)
                else:
                    label = '{}: OFF'.format(text)
            if self.true_label and status:
                label = self.true_label
            if self.false_label and (not status):
                label = self.false_label
            layout.prop(self, "value", text=label, toggle=self.use_toggle)

    def get_unlinked_value(self):
        return "True" if self.value and self.enabled else "False"


_sockets.append(NLBooleanSocket)


class NLXYZSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLXYZSocket"
    bl_label = "Boolean"
    x: BoolProperty(update=update_tree_code, default=True)
    y: BoolProperty(update=update_tree_code, default=True)
    z: BoolProperty(update=update_tree_code, default=True)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.prop(self, 'x', text="X")
            row.prop(self, 'y', text="Y")
            row.prop(self, 'z', text="Z")

    def get_unlinked_value(self):
        return "dict(x={}, y={}, z={})".format(self.x, self.y, self.z)


_sockets.append(NLXYZSocket)


class NLInvertedXYSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Boolean"
    x: BoolProperty(update=update_tree_code)
    y: BoolProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text='Inverted:')
            row.prop(self, 'x', text="X")
            row.prop(self, 'y', text="Y")

    def get_unlinked_value(self):
        return "dict(x={}, y={})".format(self.x, self.y)


_sockets.append(NLInvertedXYSocket)


class NLPositiveFloatSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveFloatSocket"
    bl_label = "Positive Float"
    value: FloatProperty(min=0.0, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLPositiveFloatSocket)


class NLPositiveStepFloat(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveStepFloat"
    bl_label = "Float"
    value: FloatProperty(min=1, default=1, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLPositiveStepFloat)


class NLPosFloatFormatSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPosFloatFormatSocket"
    bl_label = "Positive Float"
    value: FloatProperty(min=0.0, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            col.label(text=text)
            col.prop(self, "value", text='')

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLPosFloatFormatSocket)


class NLSocketOptionalPositiveFloat(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketOptionalPositiveFloat"
    bl_label = "Positive Float"
    use_this: BoolProperty(update=update_tree_code)
    value: StringProperty(update=update_tree_code)

    def update_value(self, context):
        if self.use_this:
            self.value = '{}'.format(self.float_editor)
        else:
            self.value = ""

        update_tree_code(self, context)

    float_editor: FloatProperty(
        min=0.0,
        update=update_value
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, 'use_this', text=text)
            if self.use_this:
                layout.prop(self, "float_editor", text=text)

    def get_unlinked_value(self):
        try:
            return '{}'.format(float(self.value))
        except ValueError:
            return "None"


_sockets.append(NLSocketOptionalPositiveFloat)


class NLSocketIKMode(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketIKMode"
    bl_label = "IK Mode"
    value: EnumProperty(
        name='IK Mode',
        items=_enum_ik_mode_values,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return f'{self.value}'


_sockets.append(NLSocketIKMode)


class NLQuotedStringFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLQuotedStringFieldSocket"
    bl_label = "String"
    value: StringProperty(update=update_tree_code)
    formatted: BoolProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        elif not text:
            layout.prop(self, "value", text='')
        else:
            if self.formatted:
                col = layout.column()
                row1 = col.row()
                row1.label(text=text)
                row2 = col.row()
                row2.prop(self, 'value', text='')
            else:
                parts = layout.split(factor=.4)
                parts.label(text=text)
                parts.prop(self, "value", text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLQuotedStringFieldSocket)


class NLFilePathSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFilePathSocket"
    bl_label = "String"
    value: StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                col.label(text=text)
            col.prop(self, "value", text='')

    def get_unlinked_value(self):
        path = str(self.value)
        path = path.replace('\\', '/')
        if path.endswith('\\'):
            path = path[:-1]
        return '"{}"'.format(path)


_sockets.append(NLFilePathSocket)


class NLIntegerFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLIntegerFieldSocket"
    bl_label = "Integer"
    value: IntProperty(update=update_tree_code)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def get_unlinked_value(self):
        return '{}'.format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
    pass


_sockets.append(NLIntegerFieldSocket)


class NLPositiveIntegerFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveIntegerFieldSocket"
    bl_label = "Integer"
    value: IntProperty(min=0, default=0, update=update_tree_code)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLPositiveIntegerFieldSocket)


class NLCountSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLCountSocket"
    bl_label = "Integer"
    value: IntProperty(min=1, default=1, update=update_tree_code)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLCountSocket)


class NLPositiveIntCentSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPositiveIntCentSocket"
    bl_label = "Integer"
    value: IntProperty(
        min=0,
        max=100,
        default=0,
        update=update_tree_code
    )
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        return '{}'.format(self.value)


_sockets.append(NLPositiveIntCentSocket)


class NLValueFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLValueFieldSocket"
    bl_label = "Value"
    value: StringProperty(update=update_tree_code)

    def on_type_changed(self, context):
        if self.value_type == "BOOLEAN":
            self.value = str(self.bool_editor)
        if self.value_type == "STRING":
            self.value = str(self.string_editor)
        if self.value_type == "FILE_PATH":
            self.value = str(self.path_editor)
        update_tree_code(self, context)

    value_type: EnumProperty(
        name='Type',
        items=_enum_field_value_types,
        update=on_type_changed
    )

    def store_boolean_value(self, context):
        self.value = str(self.bool_editor)
        update_tree_code(self, context)

    bool_editor: BoolProperty(update=store_boolean_value)

    def store_int_value(self, context):
        self.value = str(self.int_editor)

    int_editor: IntProperty(update=store_int_value)

    def store_float_value(self, context):
        self.value = str(self.float_editor)

    float_editor: FloatProperty(update=store_float_value)

    def store_string_value(self, context):
        self.value = self.string_editor

    string_editor: StringProperty(update=store_string_value)

    def store_path_value(self, context):
        self.value = self.path_editor

    path_editor: StringProperty(
        update=store_path_value,
        subtype='FILE_PATH'
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return socket_field(self)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                name_row = col.row()
                name_row.label(text=text)
            val_line = col.row()
            val_row = val_line.split()
            if self.value_type == "BOOLEAN":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "bool_editor", text="")
            elif self.value_type == "INTEGER":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "int_editor", text="")
            elif self.value_type == "FLOAT":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "float_editor", text="")
            elif self.value_type == "STRING":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "string_editor", text="")
            elif self.value_type == "FILE_PATH":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "path_editor", text="")


_sockets.append(NLValueFieldSocket)


class NLOptionalValueFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLOptionalValueFieldSocket"
    bl_label = "Value"
    value: StringProperty(update=update_tree_code)

    def on_type_changed(self, context):
        if self.value_type == "BOOLEAN":
            self.value = str(self.bool_editor)
        if self.value_type == "STRING":
            self.value = str(self.string_editor)
        if self.value_type == "FILE_PATH":
            self.value = str(self.path_editor)
        update_tree_code(self, context)

    value_type: EnumProperty(
        name='Type',
        items=_enum_field_value_types,
        update=on_type_changed
    )

    use_value: BoolProperty(
        update=update_tree_code
    )

    def store_boolean_value(self, context):
        self.value = str(self.bool_editor)
        update_tree_code(self, context)

    bool_editor: BoolProperty(update=store_boolean_value)

    def store_int_value(self, context):
        self.value = str(self.int_editor)

    int_editor: IntProperty(update=store_int_value)

    def store_float_value(self, context):
        self.value = str(self.float_editor)

    float_editor: FloatProperty(update=store_float_value)

    def store_string_value(self, context):
        self.value = self.string_editor

    string_editor: StringProperty(update=store_string_value)

    def store_path_value(self, context):
        self.value = self.path_editor

    path_editor: StringProperty(
        update=store_path_value,
        subtype='FILE_PATH'
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return socket_field(self) if self.use_value or self.is_linked else "utils.STATUS_INVALID"

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                name_row = col.row()
                name_row.label(text=text)
                name_row.prop(self, "use_value", text="")
            if not self.use_value:
                return
            val_line = col.row()
            val_row = val_line.split()
            if self.value_type == "BOOLEAN":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "bool_editor", text="")
            elif self.value_type == "INTEGER":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "int_editor", text="")
            elif self.value_type == "FLOAT":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "float_editor", text="")
            elif self.value_type == "STRING":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "string_editor", text="")
            elif self.value_type == "FILE_PATH":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "path_editor", text="")


_sockets.append(NLOptionalValueFieldSocket)


class NLNumericFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLNumericFieldSocket"
    bl_label = "Value"

    value_type: EnumProperty(
        name='Type',
        items=_enum_numeric_field_value_types,
        update=update_tree_code
    )
    value: StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return socket_field(self)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            split = layout.split(factor=0.4)
            split.label(text=text)
            if self.value_type == "NONE":
                split.prop(self, "value_type", text="")
            else:
                row = split.row(align=True)
                row.prop(self, "value_type", text="")
                row.prop(self, "value", text="")


_sockets.append(NLNumericFieldSocket)


class NLOptionalRadiansFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLOptionalRadiansFieldSocket"
    bl_label = "Value"
    value: StringProperty(update=update_tree_code, default="0.0")

    def store_radians(self, context):
        self.radians = str(float(self.float_field))
        update_tree_code(self, context)

    def store_expression(self, context):
        self.radians = self.string_field
        update_tree_code(self, context)

    def on_type_change(self, context):
        if self.type == "NONE":
            self.radians = "None"
        if self.type == "EXPRESSION":
            self.radians = self.expression_field
        if self.type == "FLOAT":
            self.radians = str(float(self.input_field))
        update_tree_code(self, context)
    float_field: FloatProperty(update=store_radians)
    expression_field: StringProperty(update=store_expression)
    input_type: EnumProperty(
        name='Type',
        items=_enum_optional_float_value_types,
        update=on_type_change, default="FLOAT"
    )

    def draw_color(self, context, node): return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "None" if self.input_type == "NONE" else self.radians

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            if self.input_type == "FLOAT":
                row = layout.split(factor=0.6)
                row.prop(self, "float_field", text=text)
                row.prop(self, "input_type", text="")
            elif self.input_type == "EXPRESSION":
                row = layout.split(factor=0.6)
                row.prop(self, "expression_field", text=text)
                row.prop(self, "input_type", text="")
            else:
                layout.prop(self, "input_type", text=text)


_sockets.append(NLOptionalRadiansFieldSocket)


class NLSocketReadableMemberName(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketReadableMemberName"
    bl_label = "Att. Name"
    value: StringProperty(
        update=update_tree_code,
        default='worldPosition'
    )
    type: StringProperty(default='VECTOR')

    def _set_value(self, context):
        t = self.value_type
        if t == "CUSTOM":
            self.value = ""
        else:
            self.value = t
        bge_netlogic.update_current_tree_code()
    value_type: EnumProperty(
        name='Attribute',
        items=_enum_readable_member_names,
        update=_set_value
    )

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR if (
            self.value != 'name' and
            self.value != 'visible'
        ) else PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            if self.value_type == "CUSTOM":
                row = layout.row(align=True)
                row.prop(self, "value_type", text="")
                row.prop(self, "value", text="")
                pass
            else:
                layout.prop(self, "value_type", text="")


_sockets.append(NLSocketReadableMemberName)


class NLKeyboardKeySocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLKeyboardKeySocket"
    bl_label = "Key"
    value: StringProperty(update=update_tree_code)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def get_unlinked_value(self):
        return keyboard_key_string_to_bge_key(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = self.value
            if not label:
                label = "Press & Choose"
            layout.operator("bge_netlogic.waitforkey", text=label)


_sockets.append(NLKeyboardKeySocket)


class NLMouseButtonSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLMouseButtonSocket"
    bl_label = "Mouse Button"
    value: EnumProperty(
        name='Button',
        items=_enum_mouse_buttons, default="bge.events.LEFTMOUSE",
        update=update_tree_code)
    type: StringProperty(default='INT')
    nl_color = PARAM_INT_SOCKET_COLOR

    def get_unlinked_value(self):
        return self.value

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")


_sockets.append(NLMouseButtonSocket)


class NLVSyncSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVSyncSocket"
    bl_label = "Vsync"
    value: EnumProperty(
        name='Mode',
        items=_enum_vsync_modes, default="bge.render.VSYNC_OFF",
        update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return self.value

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")


_sockets.append(NLVSyncSocket)


class NLPlayActionModeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLPlayActionModeSocket"
    bl_label = "Play Mode"
    value: EnumProperty(
        name='Mode',
        items=_enum_play_mode_values,
        description="The play mode of the action",
        update=update_tree_code
    )

    def get_unlinked_value(self):
        return self.value

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLPlayActionModeSocket)

### LOak MOD FROM HERE
class NLFloatFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFloatFieldSocket"
    bl_label = "Float Value"
    value: FloatProperty(default=0, update=update_tree_code)
    valid_sockets = ['NLFloatFieldSocket']

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLFloatFieldSocket)


class NLFloatAngleSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLFloatAngleSocket"
    bl_label = "Float Value"
    value: FloatProperty(default=0, update=update_tree_code, unit='ROTATION')
    valid_sockets = ['NLFloatFieldSocket']

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLFloatAngleSocket)


class NLTimeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTimeSocket"
    bl_label = "Float Value"
    value: FloatProperty(
        min=0,
        default=0,
        subtype='TIME',
        unit='TIME',
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLTimeSocket)

#:# LOak
class NLVec2FieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVec2FieldSocket"
    bl_label = "Float Value"
    value_x: FloatProperty(default=0, update=update_tree_code)
    value_y: FloatProperty(default=0, update=update_tree_code)
    title: StringProperty(default='')
    type: StringProperty(default='VECTOR')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}))".format(self.value_x, self.value_y)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            if text != '':
                column.label(text=text)
            row = column.row(align=True)
            row.prop(self, "value_x", text='')
            row.prop(self, "value_y", text='')


_sockets.append(NLVec2FieldSocket)


class NLAngleLimitSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLAngleLimitSocket"
    bl_label = "Float Value"
    type: StringProperty(default='VECTOR')
    value_x: FloatProperty(
        default=0,
        unit='ROTATION',
        update=update_tree_code
    )
    value_y: FloatProperty(
        default=0,
        unit='ROTATION',
        update=update_tree_code
    )
    title: StringProperty(default='')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}))".format(self.value_x, self.value_y)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            if text != '':
                column.label(text=text)
            row = column.row(align=True)
            row.prop(self, "value_x", text='')
            row.prop(self, "value_y", text='')


_sockets.append(NLAngleLimitSocket)


class NLVec2PositiveFieldSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVec2PositiveFieldSocket"
    bl_label = "Float Value"
    value_x: FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    value_y: FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    title: StringProperty(default='')
    type: StringProperty(default='VECTOR')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}))".format(self.value_x, self.value_y)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            # if self.title != '':
            #     title = column.label(text=self.title)
            row = column.row(align=True)
            row.prop(self, "value_x", text='')
            row.prop(self, "value_y", text='')


_sockets.append(NLVec2PositiveFieldSocket)

#:#:#: These are Vec3d-Sockets
#: THUS     all of them do update=update_tree_code,
#:                      have type=StringProperty("VECTOR")
# NOTE: one might need to take a look into the addon update functionality
#       Then again, that might be necessarry anyways.
class NLVec3FieldSocket(bpy.types.NodeSocket, _NLSocket_Vec3):
    bl_idname = "NLVec3FieldSocket"
    value: FloatVectorProperty(default=(0,0,0), update=update_tree_code)

class NodeSocketMatrix3(bpy.types.NodeSocket, _NLSocket_Vec3):
    bl_idname = "NodeSocketMatrix3"
    value: FloatVectorProperty(default=(0,0,0), update=update_tree_code)

class NLVec3RotationSocket(bpy.types.NodeSocket, _NLSocket_Vec3):
    bl_idname = "NLVec3RotationSocket"
    value: FloatVectorProperty(default=(0,0,0), update=update_tree_code,
                               unit='ROTATION' )

class NLVelocitySocket(bpy.types.NodeSocket, _NLSocket_Vec3):
    bl_idname = "NLVelocitySocket"
    value: FloatVectorProperty(default=(0,0,0), update=update_tree_code,
                               unit='VELOCITY' )

class NLVec3PositiveFieldSocket(bpy.types.NodeSocket, _NLSocket_Vec3):
    bl_idname = "NLVec3PositiveFieldSocket"
    value: FloatVectorProperty(default=(0,0,0), update=update_tree_code, min=0.0)
    title: StringProperty(default='') # not used anywhere

_sockets.append(NLVec3FieldSocket)
_sockets.append(NodeSocketMatrix3)
_sockets.append(NLVec3RotationSocket)
_sockets.append(NLVelocitySocket)
_sockets.append(NLVec3PositiveFieldSocket)
### END LOak Mod

class NLColorSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLColorSocket"
    bl_label = "Float Value"
    value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=3,
        default=(1.0, 1.0, 1.0),
        update=update_tree_code
    )
    type: StringProperty(default='RGBA')
    nl_color = PARAM_COLOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}))".format(
            self.value[0],
            self.value[1],
            self.value[2]
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text=text if text else 'Color')
            row.prop(self, "value", text='')


_sockets.append(NLColorSocket)


class NLColorAlphaSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLColorAlphaSocket"
    bl_label = "Float Value"
    value: FloatVectorProperty(
        subtype='COLOR_GAMMA',
        min=0.0,
        max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_tree_code
    )
    type: StringProperty(default='RGBA')
    nl_color = PARAM_COLOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}, {}))".format(
            self.value[0],
            self.value[1],
            self.value[2],
            self.value[3]
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            row = layout.row()
            row.label(text=text if text else 'Color')
            row.prop(self, "value", text='')


_sockets.append(NLColorAlphaSocket)


class NLBlendActionModeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLBlendActionMode"
    bl_label = "Blend Mode"
    value: EnumProperty(
        name='Blend Mode',
        items=_enum_blend_mode_values,
        description="The blend mode of the action",
        update=update_tree_code
    )

    def get_unlinked_value(self):
        return self.value

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLBlendActionModeSocket)


class NLVectorSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVectorSocket"
    bl_label = "Parameter"
    type: StringProperty(default='VECTOR')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLVectorSocket)


class NLSocketVectorField(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketVectorField"
    bl_label = "Vector"
    type: StringProperty(default='VECTOR')
    value: StringProperty(
        update=update_tree_code,
        description=(
            'Default to (0,0,0), '
            'type numbers separated by space or '
            'comma or anything but a dot'
        )
    )

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        return parse_field_value("VECTOR", self.value)


_sockets.append(NLSocketVectorField)


class NLOptionalSocketVectorField(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLOptionalSocketVectorField"
    bl_label = "Vector"
    type: StringProperty(default='VECTOR')
    value: StringProperty(
        update=update_tree_code,
        description=(
            'Default to None, type numbers separated by space or comma '
            'or anything but a dot'
        )
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        if not self.value:
            return "None"
        return parse_field_value("VECTOR", self.value)


_sockets.append(NLOptionalSocketVectorField)


class NLSocketOptionalFilePath(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketOptionalFilePath"
    bl_label = "File"
    value: StringProperty(
        update=update_tree_code,
        description=(
            'None if empty. Absolute or Relative path. '
            'Relative paths start with //'
        )
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        if not self.value:
            return "None"
        return '"{}"'.format(self.value)


_sockets.append(NLSocketOptionalFilePath)


class NLSocketMouseWheelDirection(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketMouseWheelDirection"
    bl_label = "Mouse Wheel"
    value: EnumProperty(
        name='Direction',
        items=_enum_mouse_wheel_direction,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        return self.value


_sockets.append(NLSocketMouseWheelDirection)


class NLSocketDistanceModels(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketDistanceModels"
    bl_label = "Distance Model"
    value: EnumProperty(
        name='Distance Model',
        items=_enum_distance_models,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            col = layout.column()
            col.label(text=text)
            col.prop(self, "value", text="")

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)


_sockets.append(NLSocketDistanceModels)


class NLVectorMathSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLVectorMathSocket"
    bl_label = "Vector Math"
    value: EnumProperty(
        name='Operation',
        items=_enum_vector_math_options,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        return "'{}'".format(self.value)


_sockets.append(NLVectorMathSocket)


class NLTypeCastSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLTypeCastSocket"
    bl_label = "Types"
    value: EnumProperty(
        name='Type',
        items=_enum_type_casts,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        return "'{}'".format(self.value)


_sockets.append(NLTypeCastSocket)


class NLConstraintTypeSocket(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLConstraintTypeSocket"
    bl_label = "Constraint Type"
    value: EnumProperty(
        name='Type',
        items=_enum_constraint_types,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        return self.value


_sockets.append(NLConstraintTypeSocket)


class NLSocketLocalAxis(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketLocalAxis"
    bl_label = "Local Axis"
    value: EnumProperty(
        name='Axis',
        items=_enum_local_axis,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "value", text='')

    def get_unlinked_value(self):
        return self.value


_sockets.append(NLSocketLocalAxis)


class NLSocketOrientedLocalAxis(bpy.types.NodeSocket, NLSocket):
    bl_idname = "NLSocketOrientedLocalAxis"
    bl_label = "Local Axis"
    value: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "value", text='')

    def get_unlinked_value(self):
        return self.value


_sockets.append(NLSocketOrientedLocalAxis)


###############################################################################
# NODES
###############################################################################


# Parameters


class NLParameterFindChildByNameNode(NLParameterNode):
    bl_idname = "NLParameterFindChildByNameNode"
    bl_label = "Get Child By Name"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Parent")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "Child")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Child")

    def get_netlogic_class_name(self):
        return "ULChildByName"

    def get_input_sockets_field_names(self):
        return ["from_parent", "child"]

    def get_output_socket_varnames(self):
        return ['CHILD']


_nodes.append(NLParameterFindChildByNameNode)


class NLParameterFindChildByIndexNode(NLParameterNode):
    bl_idname = "NLParameterFindChildByIndexNode"
    bl_label = "Get Child By Index"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Parent")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Index")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Child")

    def get_netlogic_class_name(self):
        return "ULChildByIndex"

    def get_input_sockets_field_names(self):
        return ["from_parent", "index"]

    def get_output_socket_varnames(self):
        return ['CHILD']


_nodes.append(NLParameterFindChildByIndexNode)


class NLParameterGetAttribute(NLParameterNode):
    bl_idname = "NLParameterGetAttribute"
    bl_label = "Get Object Attribute"
    nl_category = "Python"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPythonSocket.bl_idname, "Object Instance")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULGetPyInstanceAttr"

    def get_input_sockets_field_names(self):
        return ['instance', 'attr']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLParameterGetAttribute)


class NLGetVRControllerValues(NLParameterNode):
    bl_idname = "NLGetVRControllerValues"
    bl_label = "VR Controller"
    nl_category = "Input"
    nl_subcat = 'VR'
    nl_module = 'parameters'
    index: EnumProperty(
        name='Controller',
        items=_enum_vrcontroller_trigger_operators,
        default='0',
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "index", text="")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Position")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Orientation")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Aim Position")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Aim Orientation")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "Thumbstick")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Trigger")

    def get_netlogic_class_name(self):
        return "ULGetVRControllerValues"

    def get_attributes(self):
        return [("index", lambda: f'{self.index}')]

    def get_output_socket_varnames(self):
        return ['POS', 'ORI', 'APOS', 'AORI', 'STICK', 'TRIGGER']


_nodes.append(NLGetVRControllerValues)


class NLGetVRHeadsetValues(NLParameterNode):
    bl_idname = "NLGetVRHeadsetValues"
    bl_label = "VR Headset"
    nl_category = "Input"
    nl_subcat = 'VR'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Position")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Orientation")

    def get_netlogic_class_name(self):
        return "ULGetVRHeadsetValues"

    def get_output_socket_varnames(self):
        return ['POS', 'ORI']


_nodes.append(NLGetVRHeadsetValues)


class NLGetScene(NLParameterNode):
    bl_idname = "NLGetScene"
    bl_label = "Get Scene"
    nl_category = "Scene"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLSceneSocket.bl_idname, "Scene")

    def get_netlogic_class_name(self):
        return "ULGetScene"

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetScene)


class NLParameterGetTimeScale(NLParameterNode):
    bl_idname = "NLParameterGetTimeScale"
    bl_label = "Get Timescale"
    nl_category = "Scene"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Timescale")

    def get_netlogic_class_name(self):
        return "ULGetTimeScale"

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLParameterGetTimeScale)


class NLParameterScreenPosition(NLParameterNode):
    bl_idname = "NLParameterScreenPosition"
    bl_label = "Screen Position"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object / Vector 3")
        self.inputs.new(NLCameraSocket.bl_idname, "Camera")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "Screen X")

    def get_netlogic_class_name(self):
        return "ULScreenPosition"

    def get_input_sockets_field_names(self):
        return ["game_object", "camera"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterScreenPosition)


class NLParameterWorldPosition(NLParameterNode):
    bl_idname = "NLParameterWorldPosition"
    bl_label = "World Position"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCameraSocket.bl_idname, "Camera")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen X")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen Y")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Depth")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "World Position")

    def get_netlogic_class_name(self):
        return "ULWorldPosition"

    def get_input_sockets_field_names(self):
        return ["camera", "screen_x", "screen_y", "world_z"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterWorldPosition)


class NLCursorBehavior(NLActionNode):
    bl_idname = "NLCursorBehavior"
    bl_label = "Cursor Behaviour"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Cursor")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Distance")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULCursorBehavior"

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return ["condition", "cursor_object", "world_z"]


_nodes.append(NLCursorBehavior)


class LogicNodeSetCustomCursor(NLActionNode):
    bl_idname = "LogicNodeSetCustomCursor"
    bl_label = "Set Custom Cursor"
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs[-1].description = 'Execution Condition'
        self.inputs.new(NLImageSocket.bl_idname, "Texture")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Size")
        self.inputs[-1].value_x = 30
        self.inputs[-1].value_y = 30
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Cursor")

    def get_netlogic_class_name(self):
        return "ULSetCustomCursor"

    def get_output_socket_varnames(self):
        return ["OUT", 'CURSOR']

    def get_input_sockets_field_names(self):
        return ["condition", "texture", "size"]


_nodes.append(LogicNodeSetCustomCursor)


class LogicNodeCreateUICanvas(NLActionNode):
    bl_idname = "LogicNodeCreateUICanvas"
    bl_label = "Create Canvas"
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Canvas")

    def get_netlogic_class_name(self):
        return "ULCreateUICanvas"

    def get_output_socket_varnames(self):
        return ["OUT", 'CANVAS']

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(LogicNodeCreateUICanvas)


_writeable_widget_attrs = [
    ("show", "Visibility", "Visibility of Widget and its children"),#
    ("bg_color", "Color", "Background color"),#
    ("opacity", "Opacity", "Opacity"),#
    ("pos", "Position", "Widget Position (0-1 if set to relative)"),#
    ("size", "Size", "Widget Size (0-1 if set to relative)"),#
    ("angle", "Angle", "Widget Angle in degrees"),#
    ("width", "Width", "Widget Width (0-1 if set to relative)"),#
    ("height", "Height", "Widget Height (0-1 if set to relative)"),#
    ("use_clipping", "Clipping", "Cut off child widgets if they go over the edges"),#
    ("halign", "X Align", "Positioning direction along the X axis (Left-Right)"),#
    ("valign", "Y Align", "Positioning direction along the Y axis (Top-Bottom)"),#
    None,
    ("border_width", "Border Width", "Border draw width"),#
    ("border_color", "Border Color", "Border draw color"),#
    None,
    ("orientation", "Orientation", "Child widget arrangement mode (BoxLayout only)"),#
    ("spacing", "Spacing", "Pixels in between child widgets (BoxLayout only)"),#
    None,
    ("hover_color", "Hover Color", "Color for when the mouse is over widget (Button only)"),#
    None,
    ("text", "Text", "Text (Label only)"),#
    ("font", "Font", "Font to use for this label (Label only)"),
    ("font_color", "Font Color", "Font Color (Label only)"),#
    ("font_size", "Font Size", "Font Size (Label only)"),#
    ("font_opacity", "Font Opacity", "Font Opacity (Label Only)"),#
    ("line_height", "Line Height", "Line Height as factor (1 = Letter Height) (Label only)"),#
    ("text_halign", "Text X Align", "Text X Alignment (Label only)"),#
    ("text_valign", "Text Y Align", "Text Y Alignment (Label only)"),#
    ("wrap", "Word Wrap", "Use the size of this label to wrap text (Label only)"),#
    ("shadow", "Use Shadow", "Draw a shadow under the text (Label only)"),#
    ("shadow_offset", "Shadow Offset", "Offset for the shadow font (Label only)"),#
    ("shadow_color", "Shadow Color", "Color for the shadow font (Label only)"),#
    None,
    ("texture", "Image", "Texture to use as image (Image only)"),
    None,
    ("icon", "Icon", "Icon (Sprite) position on sheet (Icon only)"),
    ("rows", "Rows", "Rows in the Icon (Sprite) sheet (Icon only)"),
    ("cols", "Columns", "Columns in the Icon (Sprite) sheet (Icon only)")
]


class LogicNodeSetUIWidgetAttr(NLActionNode):
    bl_idname = "LogicNodeSetUIWidgetAttr"
    bl_label = "Set Widget Attribute"
    nl_category = "UI"
    nl_module = 'actions'
    widget_attr: EnumProperty(items=_writeable_widget_attrs, name='', update=update_draw)


    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Widget")
        self.inputs.new(NLBooleanSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLColorAlphaSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLFontSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLImageSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.inputs.new(NLFloatAngleSocket.bl_idname, "")
        self.inputs[-1].enabled = False
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_attributes(self):
        return [
            ("widget_attr", lambda: f'"{self.widget_attr}"')
        ]

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'widget_attr', text='')

    def update_draw(self):
        for ipt in self.inputs:
            ipt.enabled = False
        self.inputs[0].enabled = True
        self.inputs[1].enabled = True
        if self.widget_attr in ['show', 'use_clipping', 'wrap', 'shadow']:
            self.inputs[2].enabled = True
        elif self.widget_attr in ['bg_color', 'border_color', 'shadow_color', 'font_color', 'hover_color']:
            self.inputs[3].enabled = True
        elif self.widget_attr in ['opacity', 'font_opacity']:
            self.inputs[4].enabled = True
        elif self.widget_attr in ['pos', 'size', 'shadow_offset']:
            self.inputs[5].enabled = True
        elif self.widget_attr in ['halign', 'valign', 'text', 'text_halign', 'text_valign', 'orientation']:
            self.inputs[6].enabled = True
        elif self.widget_attr in ['spacing', 'font_size', 'icon', 'rows', 'cols', 'border_width']:
            self.inputs[7].enabled = True
        elif self.widget_attr in ['width', 'height', 'line_height']:
            self.inputs[8].enabled = True
        elif self.widget_attr in ['font']:
            self.inputs[9].enabled = True
        elif self.widget_attr in ['texture']:
            self.inputs[10].enabled = True
        elif self.widget_attr in ['angle']:
            self.inputs[11].enabled = True

    def get_netlogic_class_name(self):
        return "ULSetUIWidgetAttr"

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'widget',
            'bool_value',
            'color_value',
            'alpha_value',
            'vec2_value',
            'str_value',
            'int_value',
            'float_value',
            'font_value',
            'img_value',
            'angle_value'
        ]


_nodes.append(LogicNodeSetUIWidgetAttr)


class LogicNodeGetUIWidgetAttr(NLActionNode):
    bl_idname = "LogicNodeGetUIWidgetAttr"
    bl_label = "Get Widget Attribute"
    nl_category = "UI"
    nl_module = 'parameters'
    widget_attr: EnumProperty(items=_writeable_widget_attrs, name='', update=update_draw)


    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLUISocket.bl_idname, "Widget")
        self.outputs.new(NLBooleanSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLColorAlphaSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLSocketAlphaFloat.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLVec2FieldSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLQuotedStringFieldSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLIntegerFieldSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLFloatFieldSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLFontSocket.bl_idname, "")
        self.outputs[-1].enabled = False
        self.outputs.new(NLImageSocket.bl_idname, "")
        self.outputs[-1].enabled = False

    def get_attributes(self):
        return [
            ("widget_attr", lambda: f'"{self.widget_attr}"')
        ]

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'widget_attr', text='')

    def update_draw(self):
        for ipt in self.outputs:
            ipt.enabled = False
        if self.widget_attr in ['show', 'use_clipping', 'wrap', 'shadow']:
            self.outputs[0].enabled = True
        elif self.widget_attr in ['color', 'border_color', 'shadow_color', 'font_color', 'hover_color']:
            self.outputs[1].enabled = True
        elif self.widget_attr in ['opacity', 'font_opacity']:
            self.outputs[2].enabled = True
        elif self.widget_attr in ['pos', 'size', 'shadow_offset']:
            self.outputs[3].enabled = True
        elif self.widget_attr in ['halign', 'valign', 'text', 'text_halign', 'text_valign', 'orientation']:
            self.outputs[4].enabled = True
        elif self.widget_attr in ['spacing', 'font_size', 'icon', 'rows', 'cols', 'border_width']:
            self.outputs[5].enabled = True
        elif self.widget_attr in ['width', 'height', 'line_height']:
            self.outputs[6].enabled = True
        elif self.widget_attr in ['font']:
            self.outputs[7].enabled = True
        elif self.widget_attr in ['texture']:
            self.outputs[8].enabled = True

    def get_netlogic_class_name(self):
        return "ULGetUIWidgetAttr"

    def get_output_socket_varnames(self):
        return ['BOOL', 'COLOR', 'ALPHA', 'VEC2', 'STR', 'INT', 'FLOAT', 'FONT', 'IMG']

    def get_input_sockets_field_names(self):
        return [
            'widget'
        ]


_nodes.append(LogicNodeGetUIWidgetAttr)


class LogicNodeAddUIWidget(NLActionNode):
    bl_idname = "LogicNodeAddUIWidget"
    bl_label = "Add Widget"
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLUISocket.bl_idname, "Widget")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULAddUIWidget"

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return ["condition", 'parent_widget', 'child_widget']


_nodes.append(LogicNodeAddUIWidget)


_ui_layout_types = [
    ("FloatLayout", "Float Layout", "A Layout that places its child widgets independent of its own position"),
    ("RelativeLayout", "Relative Layout", "A Layout that places its child widgets relative to its own position"),
    ("BoxLayout", "Box Layout", "A Layout that automatically places widgets in either rows or columns")
]

_ui_boxlayout_types = [
    ("vertical", "Vertical", "Arrange child widgets horizontally"),
    ("horizontal", "Horizontal", "Arrange child widgets horizontally")
]

_ui_slider_types = [
    ("0", "Simple", "A knob sliding along a thin bar"),
    ("1", "Framed", "A knob sliding inside a frame"),
    ("2", "Progress", "A frame filled with color corresponding to knob position")
]

_ui_halign_types = [
    ("left", "Left", "Start positioning from the left side of the widget"),
    ("center", "Center", "Use the position as horizontal center"),
    ("right", "Right", "Start positioning from the right side of the widget")
]

_ui_valign_types = [
    ("bottom", "Bottom", "Start positioning from the bottom side of the widget"),
    ("center", "Center", "Use the position as vertical center"),
    ("top", "Top", "Start positioning from the top side of the widget")
]


class LogicNodeCreateUILayout(NLActionNode):
    bl_idname = "LogicNodeCreateUILayout"
    bl_label = "Create Layout"
    nl_subcat = 'Widgets'
    nl_category = "UI"
    nl_module = 'actions'
    layout_type: EnumProperty(items=_ui_layout_types, name='Layout Type', update=update_draw)
    boxlayout_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Position")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Size")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs[-1].value_x = 100
        self.inputs[-1].value_y = 100
        self.inputs.new(NLFloatAngleSocket.bl_idname, "Angle")
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Color")
        self.inputs[-1].value = [0, 0, 0, 0]
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Border Width")
        self.inputs[-1].value = 1
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Border Color")
        self.inputs[-1].value = [0, 0, 0, 0]
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Spacing")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Layout")

    def update_draw(self):
        self.inputs[10].enabled = (self.layout_type == 'BoxLayout')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'layout_type', text='')
        if self.layout_type == 'BoxLayout':
            layout.prop(self, 'boxlayout_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def get_netlogic_class_name(self):
        return "ULCreateUILayout"

    def get_output_socket_varnames(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("layout_type", lambda: f'"{self.layout_type}"'),
            ("boxlayout_type", lambda: f'"{self.boxlayout_type}"'),
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"')
        ]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "rel_size",
            "size",
            "angle",
            "color",
            "border_width",
            "border_color",
            'spacing'
        ]


_nodes.append(LogicNodeCreateUILayout)


class LogicNodeCreateUIButton(NLActionNode):
    bl_idname = "LogicNodeCreateUIButton"
    bl_label = "Create Button"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')
    text_halign_type: EnumProperty(items=_ui_halign_types, name='Text X', default='center')
    text_valign_type: EnumProperty(items=_ui_valign_types, name='Text Y', default='center')

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Position")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Size")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs[-1].value_x = 100
        self.inputs[-1].value_y = 100
        self.inputs.new(NLFloatAngleSocket.bl_idname, "Angle")
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Color")
        self.inputs[-1].value = [0, 0, 0, 0]
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Hover Color")
        self.inputs[-1].value = [0, 0, 0, .5]
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Border Width")
        self.inputs[-1].value = 1
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Border Color")
        self.inputs[-1].value = [0, 0, 0, 0]
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Text")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Text Position")
        self.inputs[-1].value_x = .5
        self.inputs[-1].value_y = .5
        self.inputs.new(NLFontSocket.bl_idname, "Font")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Font Size")
        self.inputs[-1].value = 12
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Line Height")
        self.inputs[-1].value = 1.5
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Font Color")
        self.inputs[-1].value = [1, 1, 1, 1]
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Button")
        self.outputs.new(NLConditionSocket.bl_idname, "On Click")
        self.outputs.new(NLConditionSocket.bl_idname, "On Hover")
        self.outputs.new(NLConditionSocket.bl_idname, "On Release")

    def update_draw(self):
        has_text = True if self.inputs[11].value else False
        for ipt in [12, 13, 14, 15, 16]:
            self.inputs[ipt].enabled = has_text

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')
        if self.inputs[11].value:
            layout.prop(self, 'text_halign_type', text='Text X')
            layout.prop(self, 'text_valign_type', text='Text Y')

    def get_netlogic_class_name(self):
        return "ULCreateUIButton"

    def get_output_socket_varnames(self):
        return ["OUT", 'WIDGET', 'CLICK', 'HOVER', 'RELEASE']

    def get_attributes(self):
        return [
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"'),
            ("text_halign_type", lambda: f'"{self.text_halign_type}"'),
            ("text_valign_type", lambda: f'"{self.text_valign_type}"')
        ]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "rel_size",
            "size",
            "angle",
            "color",
            "hover_color",
            "border_width",
            "border_color",
            "text",
            "text_pos",
            "font",
            "font_size",
            "line_height",
            "font_color"
        ]


_nodes.append(LogicNodeCreateUIButton)


class LogicNodeCreateUILabel(NLActionNode):
    bl_idname = "LogicNodeCreateUILabel"
    bl_label = "Create Label"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Position")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLFloatAngleSocket.bl_idname, "Angle")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Text")
        self.inputs.new(NLFontSocket.bl_idname, "")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Font Size")
        self.inputs[-1].value = 12
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Line Height")
        self.inputs[-1].value = 1.5
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Font Color")
        self.inputs[-1].value = [1, 1, 1, 1]
        self.inputs.new(NLBooleanSocket.bl_idname, "Use Shadow")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Shadow Offset")
        self.inputs[-1].value_x = 1
        self.inputs[-1].value_y = -1
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Shadow Color")
        self.inputs[-1].value = [0, 0, 0, .5]
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Label")

    def update_draw(self):
        shadow = self.inputs[10].value
        self.inputs[11].enabled = shadow
        self.inputs[12].enabled = shadow

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def get_netlogic_class_name(self):
        return "ULCreateUILabel"

    def get_output_socket_varnames(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"')
        ]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "angle",
            "text",
            "font",
            "font_size",
            "line_height",
            "font_color",
            "use_shadow",
            "shadow_offset",
            "shadow_color",
        ]


_nodes.append(LogicNodeCreateUILabel)


class LogicNodeCreateUISlider(NLActionNode):
    bl_idname = "LogicNodeCreateUISlider"
    bl_label = "Create Slider"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    slider_type: EnumProperty(items=_ui_slider_types, name='Type', update=update_draw)
    orientation_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation', default='horizontal')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Position")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Size")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs[-1].value_x = 200
        self.inputs[-1].value_y = 10
        self.inputs.new(NLFloatAngleSocket.bl_idname, "Angle")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Bar Width")
        self.inputs[-1].value = .5
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Border Width")
        self.inputs[-1].value = 1
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Border Color")
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Bar Color")
        self.inputs[-1].value = (.1, .1, .1, .5)
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Bar Hover Color")
        self.inputs[-1].value = (.1, .1, .1, .7)
        self.inputs.new(NLImageSocket.bl_idname, "Bar Texture")
        self.inputs[-1].enabled = False
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Knob Size")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Knob Color")
        self.inputs[-1].value = (.7, .8, 1., 1.)
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Knob Hover Color")
        self.inputs.new(NLImageSocket.bl_idname, "Knob Texture")
        self.inputs[-1].enabled = False
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Steps")
        self.inputs.new(NLBooleanSocket.bl_idname, "Bar Control")
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Label")
        self.outputs.new(NLParameterSocket.bl_idname, "Slider Value")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "Knob Position")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'slider_type', text='')
        layout.prop(self, 'orientation_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def update_draw(self):
        self.inputs[7].enabled = self.slider_type == '0'
        self.inputs[8].enabled = not self.inputs[7].enabled
        self.inputs[15].enabled = self.inputs[7].enabled

    def get_netlogic_class_name(self):
        return "ULCreateUISlider"

    def get_output_socket_varnames(self):
        return ["OUT", 'WIDGET', 'VALUE', 'KNOB_POSITION']

    def get_attributes(self):
        return [
            ("orientation_type", lambda: f'"{self.orientation_type}"'),
            ("slider_type", lambda: f'"{self.slider_type}"'),
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"')
        ]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            'pos',
            'rel_size',
            'size',
            'angle',
            'bar_width',
            'border_width',
            'border_color',
            'bar_color',
            'bar_hover_color',
            'bar_texture',
            'knob_size',
            'knob_color',
            'knob_hover_color',
            'knob_texture',
            'steps',
            'allow_bar_click'
        ]


_nodes.append(LogicNodeCreateUISlider)


class LogicNodeCreateUIImage(NLActionNode):
    bl_idname = "LogicNodeCreateUIImage"
    bl_label = "Create Image"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLUISocket.bl_idname, "Parent")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Position")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Relative Size")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.inputs.new(NLFloatAngleSocket.bl_idname, "Angle")
        self.inputs.new(NLImageSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLUISocket.bl_idname, "Label")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def get_netlogic_class_name(self):
        return "ULCreateUIImage"

    def get_output_socket_varnames(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"')
        ]

    def get_input_sockets_field_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "rel_size",
            "size",
            "angle",
            "texture"
        ]


_nodes.append(LogicNodeCreateUIImage)


class NLOwnerGameObjectParameterNode(NLParameterNode):
    """The owner of this logic tree.
    Each Object that has this tree installed is
    the "owner" of a logic tree
    """
    bl_idname = "NLOwnerGameObjectParameterNode"
    bl_label = "Get Owner"
    bl_icon = 'USER'
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLGameObjectSocket.bl_idname, "Owner Object")

    def get_netlogic_class_name(self):
        return "ULGetOwner"


_nodes.append(NLOwnerGameObjectParameterNode)


class NLGetVsyncNode(NLParameterNode):
    bl_idname = "NLGetVsyncNode"
    bl_label = "Get VSync"
    nl_category = 'Render'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Mode")

    def get_netlogic_class_name(self):
        return "ULGetVSync"

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetVsyncNode)


class NLGetFullscreen(NLParameterNode):
    bl_idname = "NLGetFullscreen"
    bl_label = "Get Fullscreen"
    nl_category = 'Render'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Fullscreen")

    def get_netlogic_class_name(self):
        return "ULGetFullscreen"

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetFullscreen)


class NLDrawLine(NLActionNode):
    bl_idname = "NLDrawLine"
    bl_label = "Line"
    nl_category = 'Render'
    nl_subcat = 'Draw'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, 'Condition')
        self.inputs.new(NLColorSocket.bl_idname, 'Color')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'From')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'To')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, 'Condition')
        self.inputs.new(NLColorSocket.bl_idname, 'Color')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Origin')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Width')
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_attributes(self):
        return [("use_volume_origin", lambda: f'{self.use_volume_origin}')]

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, 'Condition')
        self.inputs.new(NLColorSocket.bl_idname, 'Color')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Origin')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Length (Y)')
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Width (X)')
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Height (Z)')
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_attributes(self):
        return [("use_volume_origin", lambda: f'{self.use_volume_origin}')]

    def get_input_sockets_field_names(self):
        return ['condition', 'color', 'origin', 'length', 'width', 'height']

    def get_netlogic_class_name(self):
        return "ULDrawBox"


_nodes.append(NLDrawBox)


class NLGetResolution(NLParameterNode):
    bl_idname = "NLGetResolution"
    bl_label = "Get Resolution"
    nl_category = 'Render'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Width")
        self.outputs.new(NLParameterSocket.bl_idname, "Height")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "Resolution")

    def get_netlogic_class_name(self):
        return "ULGetResolution"

    def get_output_socket_varnames(self):
        return ['WIDTH', 'HEIGHT', 'RES']


_nodes.append(NLGetResolution)


class NLGameObjectPropertyParameterNode(NLParameterNode):
    bl_idname = "NLGameObjectPropertyParameterNode"
    bl_label = "Get Property"
    bl_icon = 'EXPORT'
    nl_category = 'Objects'
    nl_subcat = 'Properties'
    nl_module = 'parameters'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.outputs.new(NLParameterSocket.bl_idname, "Property Value")

    def get_netlogic_class_name(self):
        return "ULGetProperty"

    def get_input_sockets_field_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGameObjectPropertyParameterNode)


class NLGetGeometryNodeValue(NLParameterNode):
    bl_idname = "NLGetGeometryNodeValue"
    bl_label = "Get Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Geometry'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLGeomNodeTreeSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        tree = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
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
        return "ULGetNodeSocket"

    def get_input_sockets_field_names(self):
        return ["tree_name", 'node_name', "input_slot"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetGeometryNodeValue)


class NLGetGeometryNodeAttribute(NLParameterNode):
    bl_idname = "NLGetGeometryNodeAttribute"
    bl_label = "Get Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Geometry'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLGeomNodeTreeSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        tree = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    def get_netlogic_class_name(self):
        return "ULGetNodeAttribute"

    def get_input_sockets_field_names(self):
        return ["tree_name", 'node_name', "internal", 'attribute']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetGeometryNodeAttribute)


class NLGetNodeGroupNodeValue(NLParameterNode):
    bl_idname = "NLGetNodeGroupNodeValue"
    bl_label = "Get Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLNodeGroupSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        tree = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
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
        return "ULGetNodeSocket"

    def get_input_sockets_field_names(self):
        return ["tree_name", 'node_name', "input_slot"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetNodeGroupNodeValue)


class NLGetNodeTreeNodeAttribute(NLParameterNode):
    bl_idname = "NLGetNodeTreeNodeAttribute"
    bl_label = "Get Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLNodeGroupSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        tree = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    def get_netlogic_class_name(self):
        return "ULGetNodeAttribute"

    def get_input_sockets_field_names(self):
        return ["tree_name", 'node_name', "internal", 'attribute']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetNodeTreeNodeAttribute)


class NLGetMaterialNodeValue(NLParameterNode):
    bl_idname = "NLGetMaterialNodeValue"
    bl_label = "Get Socket Value"
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        mat = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if mat.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
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
        return "ULGetMaterialSocket"

    def get_input_sockets_field_names(self):
        return ["mat_name", 'node_name', "input_slot"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetMaterialNodeValue)


class NLGetMaterialNodeAttribute(NLParameterNode):
    bl_idname = "NLGetMaterialNodeAttribute"
    bl_label = "Get Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        mat = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    def get_netlogic_class_name(self):
        return "ULGetMaterialAttribute"

    def get_input_sockets_field_names(self):
        return ["mat_name", 'node_name', "internal", 'attribute']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetMaterialNodeAttribute)


class NLGetMaterialNode(NLParameterNode):
    bl_idname = "NLGetMaterialNode"
    bl_label = "Get Node"
    nl_category = 'Nodes'
    nl_subcat = 'Materials'
    nl_module = 'parameters'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.outputs.new(NLParameterSocket.bl_idname, "Node")

    def get_netlogic_class_name(self):
        return "ULGetMaterialNode"

    def get_input_sockets_field_names(self):
        return ["mat_name", 'node_name']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetMaterialNode)


class NLGameObjectHasPropertyParameterNode(NLParameterNode):
    bl_idname = "NLGameObjectHasPropertyParameterNode"
    bl_label = "Has Property"
    bl_icon = 'QUESTION'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'conditions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def get_netlogic_class_name(self):
        return "ULHasProperty"

    def get_input_sockets_field_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGameObjectHasPropertyParameterNode)


class NLGetDictKeyNode(NLParameterNode):
    bl_idname = "NLGetDictKeyNode"
    bl_label = 'Get Key'
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLDictSocket.bl_idname, "Dictionary")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Key")
        self.inputs[-1].value = 'key'
        self.inputs.new(NLOptionalValueFieldSocket.bl_idname, "Default Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Property Value")

    def get_netlogic_class_name(self):
        return "ULDictValue"

    def get_input_sockets_field_names(self):
        return ["dict", "key", 'default_value']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetDictKeyNode)


class NLGetRandomListIndex(NLParameterNode):
    bl_idname = "NLGetRandomListIndex"
    bl_label = "Get Random Item"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLListSocket.bl_idname, "List")# .display_shape = 'SQUARE'
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULListIndexRandom"

    def get_input_sockets_field_names(self):
        return ["items"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetRandomListIndex)


class NLDuplicateList(NLParameterNode):
    bl_idname = "NLDuplicateList"
    bl_label = "Duplicate"
    bl_icon = 'CON_TRANSLIKE'
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLListSocket.bl_idname, "List")
        self.outputs.new(NLListSocket.bl_idname, "List")

    def get_netlogic_class_name(self):
        return "ULListDuplicate"

    def get_input_sockets_field_names(self):
        return ["items"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLDuplicateList)


class NLGetListIndexNode(NLParameterNode):
    bl_idname = "NLGetListIndexNode"
    bl_label = "Get Index"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLListSocket.bl_idname, "List")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Index")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULListIndex"

    def get_input_sockets_field_names(self):
        return ["items", "index"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetListIndexNode)


class NLGetActuatorValue(NLParameterNode):
    bl_idname = "NLGetActuatorValue"
    bl_label = "Get Actuator Value"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.inputs[-1].brick_type = 'actuators'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Field")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULGetActuatorValue"

    def get_input_sockets_field_names(self):
        return ["game_obj", "act_name", 'field']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetActuatorValue)


class NLRunActuatorNode(NLActionNode):
    bl_idname = "NLRunActuatorNode"
    bl_label = "Run Actuator"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLLogicBrickSocket.bl_idname, "From Controller")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'actuators'
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRunActuator"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Sensor")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'sensors'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetSensorValue"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.inputs[-1].ref_index = 1
        self.inputs[-1].brick_type = 'actuators'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetActuatorValue"

    def get_input_sockets_field_names(self):
        return ["condition", 'game_obj', 'act_name', 'field', 'value']


_nodes.append(NLSetActuatorValueNode)


class NLVectorMath(NLParameterNode):
    bl_idname = "NLVectorMath"
    bl_label = "Vector Math"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Operation',
        items=_enum_vector_math_options,
        update=update_draw
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 1")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 2")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Scale")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 3")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "IOR")
        self.outputs.new(NLParameterSocket.bl_idname, 'Result')

    def get_netlogic_class_name(self):
        return "ULVectorMath"

    def update_draw(self):
        vtype = self.operator
        v2 = self.inputs[1]
        fac = self.inputs[2]
        sca = self.inputs[3]
        v3 = self.inputs[4]
        ior = self.inputs[5]

        v2.enabled = vtype in ['dot', 'cross', 'project', 'distance', 'faceforward', 'divide', 'multiply', 'subtract', 'add', 'lerp', 'slerp', 'multadd']
        fac.enabled = vtype in ['lerp', 'slerp']
        sca.enabled = vtype in ['scale']
        v3.enabled = vtype in ['faceforward', 'multadd', 'slerp']
        ior.enabled = vtype in ['refract']

    def get_input_sockets_field_names(self):
        return ["vector", 'vector_2', 'factor', 'scale', 'vector_3', 'ior']

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            'operator',
            text=''
        )

    def get_attributes(self):
        return [
            ("op", lambda: f'"{self.operator}"'),
        ]


_nodes.append(NLVectorMath)


class NLVectorAngle(NLParameterNode):
    bl_idname = "NLVectorAngle"
    bl_label = "Angle"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 1")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 2")
        self.outputs.new(NLParameterSocket.bl_idname, 'Angle')

    def get_netlogic_class_name(self):
        return "ULVectorAngle"

    def get_input_sockets_field_names(self):
        return ["vector", 'vector_2']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLVectorAngle)


class NLVectorAngleCheck(NLParameterNode):
    bl_idname = "NLVectorAngleCheck"
    bl_label = "Check Angle"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'
    operator: EnumProperty(
        name='Operation',
        items=_enum_logic_operators,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 1")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 2")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, 'If True')
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Angle")

    def get_netlogic_class_name(self):
        return "ULVectorAngleCheck"

    def get_input_sockets_field_names(self):
        return ["vector", 'vector_2', 'value']

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            'operator',
            text=''
        )

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLLogicBrickSocket.bl_idname, 'Sensor')
        self.inputs[-1].brick_type = 'sensors'
        self.outputs.new(NLConditionSocket.bl_idname, "Positive")

    def get_netlogic_class_name(self):
        return "ULSensorPositive"

    def get_input_sockets_field_names(self):
        return ['obj_name', 'sens_name']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLLogicBrickSocket.bl_idname, 'Controller')
        self.inputs[-1].brick_type = 'controllers'
        self.outputs.new(NLConditionSocket.bl_idname, "Status")
        self.outputs.new(NLDictSocket.bl_idname, "Sensors")

    def get_netlogic_class_name(self):
        return "ULControllerStatus"

    def get_input_sockets_field_names(self):
        return ['obj_name', 'cont_name']

    def get_output_socket_varnames(self):
        return ['OUT', 'SENSORS']


_nodes.append(NLControllerStatus)


class NLSensorValueNode(NLParameterNode):
    bl_idname = "NLSensorValueNode"
    bl_label = "Get Sensor Value"
    nl_category = 'Logic'
    nl_subcat = 'Bricks'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLLogicBrickSocket.bl_idname, 'Sensor')
        self.inputs[-1].brick_type = 'sensors'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Field')
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULGetSensorValue"

    def get_input_sockets_field_names(self):
        return ['game_obj', 'sens_name', "field"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLSensorValueNode)


class NLActionGetCharacterInfo(NLParameterNode):
    bl_idname = "NLActionGetCharacterInfo"
    bl_label = "Get Physics Info"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'parameters'
    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLIntegerFieldSocket.bl_idname, 'Max Jumps')
        self.outputs.new(NLIntegerFieldSocket.bl_idname, 'Current Jump Count')
        self.outputs.new(NLVec3FieldSocket.bl_idname, 'Gravity')
        self.outputs.new(NLVec3FieldSocket.bl_idname, 'Walk Direction')
        self.outputs.new(NLBooleanSocket.bl_idname, 'On Ground')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_netlogic_class_name(self):
        return "ULCharacterInfo"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("local", lambda: "True" if self.local else "False")]

    def get_output_socket_varnames(self):
        return ["MAX_JUMPS", "CUR_JUMP", "GRAVITY", 'WALKDIR', 'ON_GROUND']


_nodes.append(NLActionGetCharacterInfo)


class NLObjectAttributeParameterNode(NLParameterNode):
    bl_idname = "NLObjectAttributeParameterNode"
    bl_label = "Get Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Object Data'
    nl_module = 'parameters'

    names = {
        'worldPosition': 'World Position',
        'localPosition': 'Local Position',
        'worldScale': 'World Scale',
        'localScale': 'Local Scale',
        'worldLinearVelocity': 'World Linear Velocity',
        'localLinearVelocity': 'Local Linear Velocity',
        'worldAngularVelocity': 'World Angular Velocity',
        'localAngularVelocity': 'Local Angular Velocity',
        'color': 'Color',
        'worldOrientation': 'World Orientation',
        'localOrientation': 'Local Orientation'
    }

    search_tags = [
        ['Get World Position', {'attr_name': 'worldPosition'}],
        ['Get World Rotation', {'attr_name': 'worldOrientation'}],
        ['Get World Linear Velocity', {'attr_name': 'worldLinearVelocity'}],
        ['Get World Angular Velocity', {'attr_name': 'worldAngularVelocity'}],
        ['Get World Transform', {'attr_name': 'worldTransform'}],
        ['Get Local Position', {'attr_name': 'localPosition'}],
        ['Get Local Rotation', {'attr_name': 'localOrientation'}],
        ['Get Local Linear Velocity', {'attr_name': 'localLinearVelocity'}],
        ['Get Local Angular Velocity', {'attr_name': 'localAngularVelocity'}],
        ['Get Local Transform', {'attr_name': 'localTransform'}],
        ['Get Scale', {'attr_name': 'worldScale'}],
        ['Get Color', {'attr_name': 'color'}],
        ['Get Name', {'attr_name': 'name'}]
    ]

    attr_name: EnumProperty(items=_enum_readable_member_names, name="", default="worldPosition", update=update_draw)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLSocketReadableMemberName.bl_idname, "Value")
        self.inputs[-1].value = 'worldPosition'
        self.inputs[-1].enabled = False
        self.attr_name = self.inputs[-1].value
        self.outputs.new(NLParameterSocket.bl_idname, "Value")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.outputs[-1].enabled = False
        self.outputs.new(NLBooleanSocket.bl_idname, "Visible")
        self.outputs[-1].enabled = False
        self.update_draw()

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'attr_name', text="")

    def update_draw(self):
        if len(self.outputs) < 1:
            return
        if len(self.outputs) < 2:
            self.outputs[0].enabled = True
            return
        elif self.attr_name in [
            'worldPosition',
            'localPosition',
            'worldScale',
            'localScale',
            'worldLinearVelocity',
            'localLinearVelocity',
            'worldAngularVelocity',
            'localAngularVelocity',
            'color',
            'worldOrientation',
            'localOrientation',
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = True
            self.outputs[1].name = self.names[self.attr_name]
            self.outputs[2].enabled = False
        elif self.attr_name == 'visible':
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = True
        else:
            self.outputs[0].enabled = True
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False


    def get_attributes(self):
        return [
            ("attribute_name", lambda: f'"{self.attr_name}"')
        ]

    def get_netlogic_class_name(self):
        return "ULObjectAttribute"

    def get_input_sockets_field_names(self):
        return ["game_object", "_attr_name"]

    def get_output_socket_varnames(self):
        return ["VAL", "VEC", "BOOL"]


_nodes.append(NLObjectAttributeParameterNode)


class NLActiveCameraParameterNode(NLParameterNode):
    bl_idname = "NLActiveCameraParameterNode"
    bl_label = "Active Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLGameObjectSocket.bl_idname, "Camera")

    def get_netlogic_class_name(self):
        return "ULActiveCamera"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActiveCameraParameterNode)


class NLStoreValue(NLParameterNode):
    bl_idname = "NLStoreValue"
    bl_label = "Store Value"
    nl_category = "Values"
    nl_module = 'parameters'
    initialize: BoolProperty(
        name='Initialize',
        description='Store a value in the first frame to avoid NoneType issues',
        default=True
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLValueFieldSocket.bl_idname, "Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Stored Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "initialize")

    def get_attributes(self):
        return [
            ("initialize", lambda: f'{self.initialize}')
        ]

    def get_input_sockets_field_names(self):
        return ['condition', 'value']

    def get_netlogic_class_name(self):
        return "ULStoreValue"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLStoreValue)


class NLGetGravityNode(NLParameterNode):
    bl_idname = "NLGetGravityNode"
    bl_label = "Get Gravity"
    nl_category = "Scene"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Gravity")

    def get_netlogic_class_name(self):
        return "ULGetGravity"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLGetGravityNode)


class NLGetCollectionNode(NLParameterNode):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    bl_icon = 'OUTLINER_COLLECTION'
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, '')
        self.outputs.new(NLCollectionSocket.bl_idname, "Collection")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "ULGetCollection"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLGetCollectionNode)


class NLGetCollectionObjectsNode(NLParameterNode):
    bl_idname = "NLGetCollectionObjectsNode"
    bl_label = "Get Objects"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLListSocket.bl_idname, "Objects")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "ULGetCollectionObjects"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLGetCollectionObjectsNode)


class NLGetCollectionObjectNamesNode(NLParameterNode):
    bl_idname = "NLGetCollectionObjectNamesNode"
    bl_label = "Get Object Names"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLListSocket.bl_idname, "Object Names")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "ULGetCollectionObjectNames"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLGetCollectionObjectNamesNode)


class NLSetOverlayCollection(NLActionNode):
    bl_idname = "NLSetOverlayCollection"
    bl_label = "Set Overlay Collection"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLCameraSocket.bl_idname, 'Camera')
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Pass Index')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Brightness')
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Start')
        self.inputs[-1].value = .1
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Density')
        self.inputs[-1].value = 0.5
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Power')
        self.inputs[-1].value = 1.0
        self.inputs.new(NLColorSocket.bl_idname, 'Color')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(self, "filter_type")

    def get_input_sockets_field_names(self):
        return ['condition', 'pass_idx', 'brightness', 'start', 'density', 'power', 'color', 'end']

    def get_attributes(self):
        return [
            ("filter_type", lambda: f'"{self.filter_type}"')
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Pass Index')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_input_sockets_field_names(self):
        return ['condition', 'pass_idx']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Pass Index')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_input_sockets_field_names(self):
        return ['condition', 'pass_idx']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Pass Index')
        self.inputs.new(NLBooleanSocket.bl_idname, 'State')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_input_sockets_field_names(self):
        return ['condition', 'pass_idx', 'state']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_input_sockets_field_names(self):
        return ['condition', 'collection']

    def get_netlogic_class_name(self):
        return "ULRemoveOverlayCollection"


_nodes.append(NLRemoveOverlayCollection)


class NLArithmeticOpParameterNode(NLParameterNode):
    bl_idname = "NLArithmeticOpParameterNode"
    bl_label = "Math"
    nl_category = "Math"
    nl_module = 'parameters'
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "A")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "B")
        self.outputs.new(NLParameterSocket.bl_idname, "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_attributes(self):
        return [
            ("operator", lambda: f'OPERATORS.get("{self.operator}")')
        ]

    def get_netlogic_class_name(self):
        return "ULMath"

    def get_input_sockets_field_names(self):
        return ["operand_a", "operand_b"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLArithmeticOpParameterNode)


class NLThresholdNode(NLParameterNode):
    bl_idname = "NLThresholdNode"
    bl_label = "Threshold"
    nl_category = "Math"
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Operation',
        items=_enum_greater_less,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "Else 0")
        self.inputs[-1].value = True
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Threshold")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("operator", lambda: f'"{self.operator}"')
        ]

    def get_netlogic_class_name(self):
        return "ULThreshold"

    def get_input_sockets_field_names(self):
        return ['else_z', "value", "threshold"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLThresholdNode)


class NLRangedThresholdNode(NLParameterNode):
    bl_idname = "NLRangedThresholdNode"
    bl_label = "Ranged Threshold"
    nl_category = "Math"
    nl_module = 'parameters'
    operator: EnumProperty(
        items=_enum_in_or_out,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Threshold")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("operator", lambda: f'"{self.operator}"')
        ]

    def get_netlogic_class_name(self):
        return "ULRangedThreshold"

    def get_input_sockets_field_names(self):
        return ["value", "threshold"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLRangedThresholdNode)


class NLLimitRange(NLParameterNode):
    bl_idname = "NLLimitRange"
    bl_label = "Limit Range"
    nl_category = "Math"
    nl_module = 'parameters'

    operator: EnumProperty(
        items=_enum_in_or_out,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Threshold")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("operator", lambda: f'"{self.operator}"')
        ]

    def get_netlogic_class_name(self):
        return "ULLimitRange"

    def get_input_sockets_field_names(self):
        return ["value", "threshold"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLLimitRange)


class NLMapRangeNode(NLParameterNode):
    bl_idname = "NLMapRangeNode"
    bl_label = "Map Range"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "From Min")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "From Max")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, "To Min")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "To Max")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLParameterSocket.bl_idname, "Result")

    def get_netlogic_class_name(self):
        return "ULMapRange"

    def get_input_sockets_field_names(self):
        return ["value", "from_min", "from_max", "to_min", "to_max"]

    def get_output_socket_varnames(self):
        return ["OUT"]

_nodes.append(NLMapRangeNode)


class NLWithinRangeNode(NLParameterNode):
    bl_idname = "NLWithinRangeNode"
    bl_label = "Within Range"
    nl_category = "Math"
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Mode',
        items=_enum_in_or_out,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Range")
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("operator", lambda: f'"{self.operator}"')
        ]

    def get_netlogic_class_name(self):
        return "ULWithinRange"

    def get_input_sockets_field_names(self):
        return ["value", "range"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLWithinRangeNode)


class NLClampValueNode(NLParameterNode):
    bl_idname = "NLClampValueNode"
    bl_label = "Clamp"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULClamp"

    def get_input_sockets_field_names(self):
        return ["value", "range"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLClampValueNode)


class NLGetImage(NLParameterNode):
    bl_idname = "NLGetImage"
    bl_label = "Get Image"
    bl_icon = 'IMAGE_DATA'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLImageSocket.bl_idname, "Image")
        self.outputs.new(NLImageSocket.bl_idname, 'Image')

    def get_netlogic_class_name(self):
        return "ULGetImage"

    def get_input_sockets_field_names(self):
        return ["image"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetImage)


class NLGetSound(NLParameterNode):
    bl_idname = "NLGetSound"
    bl_label = "Get Sound"
    bl_icon = 'FILE_SOUND'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLSoundFileSocket.bl_idname, "Sound File")
        self.outputs.new(NLSoundFileSocket.bl_idname, 'Sound File')

    def get_netlogic_class_name(self):
        return "ULGetSound"

    def get_input_sockets_field_names(self):
        return ["sound"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLGetSound)


class LogicNodeGetFont(NLParameterNode):
    bl_idname = "LogicNodeGetFont"
    bl_label = "Get Font"
    bl_icon = 'FILE_FONT'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFontSocket.bl_idname, "Font")
        self.outputs.new(NLFontSocket.bl_idname, 'Font')

    def get_netlogic_class_name(self):
        return "ULGetFont"

    def get_input_sockets_field_names(self):
        return ["font"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(LogicNodeGetFont)


class LogicNodeSerializeData(NLParameterNode):
    bl_idname = "LogicNodeSerializeData"
    bl_label = "Serialize Data"
    bl_icon = 'ALIGN_FLUSH'
    nl_category = "Network"
    nl_module = 'parameters'

    serialize_as: EnumProperty(items=_serialize_types, name='Serialize As', description='Select the correct format to serialize a python object')

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Data")
        self.outputs.new(NLParameterSocket.bl_idname, 'Data')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'serialize_as', text='')

    def get_netlogic_class_name(self):
        return "ULSerializeData"

    def get_attributes(self):
        return [("serialize_as", lambda: f'"{self.serialize_as}"')]

    def get_input_sockets_field_names(self):
        return ["data"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(LogicNodeSerializeData)


class LogicNodeRebuildData(NLParameterNode):
    bl_idname = "LogicNodeRebuildData"
    bl_label = "Rebuild Data"
    bl_icon = 'OBJECT_HIDDEN'
    nl_category = "Network"
    nl_module = 'parameters'

    read_as: EnumProperty(items=_serialize_types, name='Read As', description='Select the correct format to read a python object')

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Data")
        self.outputs.new(NLParameterSocket.bl_idname, 'Data')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'read_as', text='')

    def get_netlogic_class_name(self):
        return "ULRebuildData"

    def get_attributes(self):
        return [("read_as", lambda: f'"{self.read_as}"')]

    def get_input_sockets_field_names(self):
        return ["data"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(LogicNodeRebuildData)


class NLInterpolateValueNode(NLParameterNode):
    bl_idname = "NLInterpolateValueNode"
    bl_label = "Interpolate"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "From")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "To")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULInterpolate"

    def get_input_sockets_field_names(self):
        return ["a", "b", "fac"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLInterpolateValueNode)


class NLParameterActionStatus(NLParameterNode):
    bl_idname = "NLParameterActionStatus"
    bl_label = "Animation Status"
    nl_category = "Animation"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.outputs.new(NLConditionSocket.bl_idname, "Is Playing")
        self.outputs.new(NLParameterSocket.bl_idname, "Action Name")
        self.outputs.new(NLParameterSocket.bl_idname, "Action Frame")

    def get_netlogic_class_name(self):
        return "ULActionStatus"

    def get_input_sockets_field_names(self):
        return ["game_object", "action_layer"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "ACTION_NAME", "ACTION_FRAME"]


_nodes.append(NLParameterActionStatus)


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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.outputs.new(NodeSocketPseudoCondition.bl_idname, "True")
        self.outputs.new(NodeSocketPseudoCondition.bl_idname, "False")

    def get_netlogic_class_name(self):
        return "ULTrueFalse"

    def get_input_sockets_field_names(self):
        return ["state"]

    def get_output_socket_varnames(self):
        return ["TRUE", "FALSE"]


_nodes.append(NLParameterSwitchValue)


class NLParameterTimeNode(NLParameterNode):
    bl_idname = "NLParameterTimeNode"
    bl_label = "Time Data"
    nl_category = 'Time'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Frames Per Second")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Time Per Frame")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Total Elapsed Time")

    def get_output_socket_varnames(self):
        return ["FPS", "TIME_PER_FRAME", "TIMELINE"]

    def get_netlogic_class_name(self):
        return "ULTimeData"


_nodes.append(NLParameterTimeNode)


class LogicNodeTimeFactor(NLParameterNode):
    bl_idname = "LogicNodeTimeFactor"
    bl_label = "Delta Factor"
    nl_category = 'Time'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Time Factor")

    def get_output_socket_varnames(self):
        return ["TIMEFACTOR"]

    def get_netlogic_class_name(self):
        return "ULFPSFactor"


_nodes.append(LogicNodeTimeFactor)


class NLMouseDataParameter(NLParameterNode):
    bl_idname = "NLMouseDataParameter"
    bl_label = "Mouse Status"
    bl_icon = 'OPTIONS'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Position")
        self.outputs.new(NLParameterSocket.bl_idname, "Movement")
        self.outputs.new(NLParameterSocket.bl_idname, "X Position")
        self.outputs.new(NLParameterSocket.bl_idname, "Y Position")
        self.outputs.new(NLParameterSocket.bl_idname, "X Movement")
        self.outputs.new(NLParameterSocket.bl_idname, "Y Movement")
        self.outputs.new(NLParameterSocket.bl_idname, "Wheel Difference")

    def get_netlogic_class_name(self):
        return "ULMouseData"

    def get_output_socket_varnames(self):
        return ["MXY0", "MDXY0", "MX", "MY", "MDX", "MDY", "MDWHEEL"]


_nodes.append(NLMouseDataParameter)


class NLParameterBoneStatus(NLParameterNode):
    bl_idname = "NLParameterBoneStatus"
    bl_label = "Bone Status"
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature Object")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "Bone Name")
        self.outputs.new(NLParameterSocket.bl_idname, "Position")
        self.outputs.new(NLParameterSocket.bl_idname, "Rotation")
        self.outputs.new(NLParameterSocket.bl_idname, "Scale")

    def get_netlogic_class_name(self):
        return "ULBoneStatus"

    def get_input_sockets_field_names(self):
        return ["armature", "bone_name"]

    def get_output_socket_varnames(self):
        return ["XYZ_POS", "XYZ_ROT", "XYZ_SCA"]


_nodes.append(NLParameterBoneStatus)


class NLParameterPythonModuleFunction(NLActionNode):
    bl_idname = "NLParameterPythonModuleFunction"
    bl_label = "Run Python Code"
    nl_category = "Python"
    nl_module = 'actions'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLTextIDSocket.bl_idname, "Module Name")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Function")
        self.inputs.new(NLListItemSocket.bl_idname, 'Argument')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLParameterSocket.bl_idname, "Returned Value")

    def get_netlogic_class_name(self):
        return "ULRunPython"

    def set_new_input_name(self):
        self.inputs[-1].name = 'Argument'

    def draw_buttons(self, context, layout):
        op = layout.operator(bge_netlogic.ops.NLAddListItemSocket.bl_idname, text='Add Argument')

    def setup(
        self,
        cell_varname,
        uids
    ):
        text = ''
        socket = 0
        while socket <= 2:
            text += self.write_socket_field_initialization(
                self.inputs[socket],
                cell_varname,
                uids
            )
            socket += 1
        items = ''
        while socket < len(self.inputs):
            field_value = None
            if self.inputs[socket].is_linked:
                field_value = self.get_linked_socket_field_value(
                    self.inputs[socket],
                    cell_varname,
                    None,
                    uids
                )
            else:
                field_value = self.inputs[socket].get_unlinked_value()
            items += f'{field_value}, '
            socket += 1
        items = items[:-2]
        line = f'        {cell_varname}.arg = [{items}]\n'
        return text + line

    def get_input_sockets_field_names(self):
        return ['condition', "module_name", 'module_func']

    def get_output_socket_varnames(self):
        return ["OUT", "VAL"]


_nodes.append(NLParameterPythonModuleFunction)


class NLParameterBooleanValue(NLParameterNode):
    bl_idname = "NLParameterBooleanValue"
    bl_label = "Boolean"
    bl_icon = 'CHECKBOX_HLT'
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "Bool")
        self.outputs.new(NLBooleanSocket.bl_idname, "Bool")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterBooleanValue)


class NLParameterFileValue(NLParameterNode):
    bl_idname = "NLParameterFileValue"
    bl_label = "File Path"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFilePathSocket.bl_idname, "")
        self.outputs.new(NLFilePathSocket.bl_idname, "Path")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterFileValue)


class NLParameterFloatValue(NLParameterNode):
    bl_idname = "NLParameterFloatValue"
    bl_label = "Float"
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Float")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterFloatValue)


class NLParameterIntValue(NLParameterNode):
    bl_idname = "NLParameterIntValue"
    bl_label = "Integer"
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "")
        self.outputs.new(NLIntegerFieldSocket.bl_idname, "Int")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterIntValue)


class NLParameterStringValue(NLParameterNode):
    bl_idname = "NLParameterStringValue"
    bl_icon = 'FONT_DATA'
    bl_label = "String"
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "")
        self.outputs.new(NLQuotedStringFieldSocket.bl_idname, "String")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterStringValue)


class NLParameterTypeCast(NLParameterNode):
    bl_idname = "NLParameterTypeCast"
    bl_label = "Typecast Value"
    nl_category = "Python"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs.new(NLTypeCastSocket.bl_idname, '')
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULTypeCastValue"

    def get_input_sockets_field_names(self):
        return ["value", 'to_type']

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterTypeCast)


class NLParameterVector2SimpleNode(NLParameterNode):
    bl_idname = "NLParameterVector2SimpleNode"
    bl_label = "Vector XY"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        utils.register_inputs(
            self,
            NLFloatFieldSocket, "X",
            NLFloatFieldSocket, "Y"
        )
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorXY"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y"]


_nodes.append(NLParameterVector2SimpleNode)


class NLParameterVector2SplitNode(NLParameterNode):
    bl_idname = "NLParameterVector2SplitNode"
    bl_label = "Separate XY"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec2FieldSocket.bl_idname, 'Vector')
        self.outputs.new(NLFloatFieldSocket.bl_idname, "X")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Y")

    def get_netlogic_class_name(self):
        return "ULVectorSplitXY"

    def get_output_socket_varnames(self):
        return ["OUTX", "OUTY"]

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLParameterVector2SplitNode)


class NLParameterVector3SplitNode(NLParameterNode):
    bl_idname = "NLParameterVector3SplitNode"
    bl_label = "Separate XYZ"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Vector')
        self.outputs.new(NLFloatFieldSocket.bl_idname, "X")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Y")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Z")

    def get_netlogic_class_name(self):
        return "ULVectorSplitXYZ"

    def get_output_socket_varnames(self):
        return ["OUTX", "OUTY", 'OUTZ']

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLParameterVector3SplitNode)


class NLParameterAbsVector3Node(NLParameterNode):
    bl_idname = "NLParameterAbsVector3Node"
    bl_label = "Absolute Vector"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        utils.register_inputs(
            self,
            NLVec3FieldSocket, 'Vector'
        )
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorAbsolute"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLParameterAbsVector3Node)


class NLVectorLength(NLParameterNode):
    bl_idname = "NLVectorLength"
    bl_label = "Vector Length"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, 'Length')
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorLength"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLVectorLength)


class NLParameterVector3SimpleNode(NLParameterNode):
    bl_idname = "NLParameterVector3SimpleNode"
    bl_label = "Vector XYZ"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'X')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Y')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Z')
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorXYZ"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z"]


_nodes.append(NLParameterVector3SimpleNode)


class NLParameterVector4SimpleNode(NLParameterNode):
    bl_idname = "NLParameterVector4SimpleNode"
    bl_label = "Vector XYZW"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'X')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Y')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Z')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'W')
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorXYZW"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z", 'input_w']


_nodes.append(NLParameterVector4SimpleNode)


class NLParameterRGBNode(NLParameterNode):
    bl_idname = "NLParameterRGBNode"
    bl_label = "Color RGB"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLColorSocket.bl_idname, 'Color')
        self.outputs.new(NLColorSocket.bl_idname, "Color")

    def get_netlogic_class_name(self):
        return "ULColorRGB"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ['color']


_nodes.append(NLParameterRGBNode)


class NLParameterRGBANode(NLParameterNode):
    bl_idname = "NLParameterRGBANode"
    bl_label = "Color RGBA"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLColorAlphaSocket.bl_idname, "Color")
        self.outputs.new(NLColorAlphaSocket.bl_idname, "Color")

    def get_netlogic_class_name(self):
        return "ULColorRGBA"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ['color']


_nodes.append(NLParameterRGBANode)


class NLParameterEulerSimpleNode(NLParameterNode):
    bl_idname = "NLParameterEulerSimpleNode"
    bl_label = "Euler"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'X')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Y')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Z')
        self.outputs.new(NLParameterSocket.bl_idname, "Euler")

    def get_netlogic_class_name(self):
        return "ULEuler"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z"]


_nodes.append(NLParameterEulerSimpleNode)


class NLParameterEulerToMatrixNode(NLParameterNode):
    bl_idname = "NLParameterEulerToMatrixNode"
    bl_label = "XYZ To Matrix"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'XYZ')
        self.outputs.new(NLParameterSocket.bl_idname, "Matrix")

    def get_netlogic_class_name(self):
        return "ULEulerToMatrix"

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return ["input_e"]


_nodes.append(NLParameterEulerToMatrixNode)


class NLParameterMatrixToEulerNode(NLParameterNode):
    bl_idname = "NLParameterMatrixToEulerNode"
    bl_label = "Matrix To XYZ"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    output: EnumProperty(
        name='Axis',
        items=_enum_vector_types,
        description="Output",
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, 'Matrix')
        self.outputs.new(NLVec3FieldSocket.bl_idname, "XYZ")

    def get_netlogic_class_name(self):
        return "ULMatrixToXYZ"

    def draw_buttons(self, context, layout):
        layout.prop(self, "output", text='')

    def update_draw(self):
        self.outputs[-1].name = 'Euler' if int(self.output) else 'Vector'

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return ["input_m"]

    def get_attributes(self):
        return [
            ("output", lambda: f'{self.output}'),
        ]


_nodes.append(NLParameterMatrixToEulerNode)


class NLOnInitConditionNode(NLConditionNode):
    bl_idname = "NLOnInitConditionNode"
    bl_label = "On Init"
    bl_icon = 'SORTBYEXT'
    nl_category = "Events"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "Init")

    def get_netlogic_class_name(self):
        return "ULOnInit"


_nodes.append(NLOnInitConditionNode)


class NLOnUpdateConditionNode(NLConditionNode):
    bl_idname = "NLOnUpdateConditionNode"
    bl_label = "On Update"
    bl_icon = 'TRIA_RIGHT'
    nl_category = "Events"
    nl_module = 'conditions'

    repeat: BoolProperty(update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "On Update")

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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Left')
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Right')
        self.inputs.new(NLTimeSocket.bl_idname, 'Time')
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULGamepadVibration"

    def get_input_sockets_field_names(self):
        return ['condition', 'index', 'left', 'right', 'time']

    def get_output_socket_varnames(self):
        return ["DONE"]


_nodes.append(NLGamepadVibration)


class NLGamepadSticksCondition(NLParameterNode):
    bl_idname = "NLGamepadSticksCondition"
    bl_label = "Sticks"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'parameters'
    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, 'Inverted')
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Sensitivity')
        self.inputs[-1].value = 1
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Threshold')
        self.inputs[-1].value = 0.05
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Left / Right")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Up / Down")

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadSticks"

    def get_input_sockets_field_names(self):
        return ['inverted', "index", 'sensitivity', 'threshold']

    def get_output_socket_varnames(self):
        return ["X", "Y"]

    def get_attributes(self):
        return [
            ("axis", lambda: f'{self.axis}')
        ]


_nodes.append(NLGamepadSticksCondition)


class NLGamepadTriggerCondition(NLParameterNode):
    bl_idname = "NLGamepadTriggerCondition"
    bl_label = "Trigger"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'parameters'
    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_trigger_operators,
        description="Left or Right Trigger",
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Sensitivity')
        self.inputs[-1].value = 1
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Threshold')
        self.inputs[-1].value = 0.05
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadTrigger"

    def get_input_sockets_field_names(self):
        return ["index", 'sensitivity', 'threshold']

    def get_output_socket_varnames(self):
        return ["VAL"]

    def get_attributes(self):
        return [
            ("axis", lambda: f'{self.axis}'),
        ]


_nodes.append(NLGamepadTriggerCondition)


class NLGamepadActive(NLConditionNode):
    bl_idname = "NLGamepadActive"
    bl_label = "Gamepad Active"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.outputs.new(NLConditionSocket.bl_idname, 'Active')

    def get_netlogic_class_name(self):
        return "ULGamepadActive"

    def get_input_sockets_field_names(self):
        return ["index"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


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
        update=update_tree_code
    )
    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_tree_code
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.outputs.new(NLConditionSocket.bl_idname, "Pressed")

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

    def get_input_sockets_field_names(self):
        return ["index"]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )
    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_tree_code
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.outputs.new(NLConditionSocket.bl_idname, "Released")

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

    def get_input_sockets_field_names(self):
        return ["index"]

    def get_output_socket_varnames(self):
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
        self.outputs.new(NLConditionSocket.bl_idname, 'Active')

    def get_netlogic_class_name(self):
        return "ULKeyboardActive"

    def get_input_sockets_field_names(self):
        return ["index"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLKeyboardKeySocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "If Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Key Down" if self.pulse else "Key Tap",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyPressed"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLParameterSocket.bl_idname, "Key Code")
        self.outputs.new(NLParameterSocket.bl_idname, "Logged Char")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Key Down" if self.pulse else "Key Tap",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyLogger"

    def get_input_sockets_field_names(self):
        return ["condition"]

    def get_output_socket_varnames(self):
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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLKeyboardKeySocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "If Released")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULKeyReleased"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLMouseButtonSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "If Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMousePressed"

    def get_input_sockets_field_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "If Moved")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMouseMoved"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLMouseButtonSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "If Released")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULMouseReleased"

    def get_input_sockets_field_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [
            ("pulse", lambda: f'{self.pulse}')
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Repeat")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Reset After')
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

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )
    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'If True')
        self.outputs.new(NLParameterSocket.bl_idname, 'Value')

    def get_netlogic_class_name(self):
        return "ULEvaluateProperty"

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLMouseButtonSocket.bl_idname, "Mouse Button")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, "When Pressed On")

    def get_netlogic_class_name(self):
        return "ULMousePressedOn"

    def get_input_sockets_field_names(self):
        return ["mouse_button", "game_object"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLConditionMousePressedOn)


class NLConditionMouseWheelMoved(NLConditionNode):
    bl_idname = "NLConditionMouseWheelMoved"
    bl_label = "Wheel"
    bl_icon = 'MOUSE_MMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLSocketMouseWheelDirection.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "When Scrolled")

    def get_netlogic_class_name(self):
        return "ULMouseScrolled"

    def get_input_sockets_field_names(self):
        return ["wheel_direction"]


_nodes.append(NLConditionMouseWheelMoved)


class NLConditionCollisionNode(NLConditionNode):
    bl_idname = "NLConditionCollisionNode"
    bl_label = "Collision"
    nl_category = "Physics"
    nl_module = 'conditions'
    pulse: BoolProperty(
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Material')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.outputs.new(NLConditionSocket.bl_idname, "When Colliding")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Colliding Object")
        self.outputs.new(NLListSocket.bl_idname, "Colliding Objects")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Point")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Normal")

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

    def get_input_sockets_field_names(self):
        return ["game_object", 'use_mat', 'prop', 'material']

    def get_output_socket_varnames(self):
        return [OUTCELL, "TARGET", "OBJECTS", "POINT", "NORMAL"]

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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Enter")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Over")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Exit")
        self.outputs.new(NLParameterSocket.bl_idname, "Point")
        self.outputs.new(NLParameterSocket.bl_idname, "Normal")

    def get_netlogic_class_name(self):
        return "ULMouseOver"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.outputs.new(NLConditionSocket.bl_idname, "If A and B")

    def get_netlogic_class_name(self):
        return "ULAnd"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.outputs.new(NLConditionSocket.bl_idname, "If A and not B")

    def get_netlogic_class_name(self):
        return "ULAndNot"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'A')
        self.inputs.new(NLConditionSocket.bl_idname, 'B')
        self.outputs.new(NLConditionSocket.bl_idname, 'A or B')

    def get_netlogic_class_name(self):
        return "ULOr"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.inputs.new(NLConditionSocket.bl_idname, "C")
        self.inputs.new(NLConditionSocket.bl_idname, "D")
        self.inputs.new(NLConditionSocket.bl_idname, "E")
        self.inputs.new(NLConditionSocket.bl_idname, "F")
        self.outputs.new(NLConditionSocket.bl_idname, "Or...")

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

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs[-1].default_value = "True"
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.inputs[-1].default_value = "True"
        self.inputs.new(NLConditionSocket.bl_idname, "C")
        self.inputs[-1].default_value = "True"
        self.inputs.new(NLConditionSocket.bl_idname, "D")
        self.inputs[-1].default_value = "True"
        self.inputs.new(NLConditionSocket.bl_idname, "E")
        self.inputs[-1].default_value = "True"
        self.inputs.new(NLConditionSocket.bl_idname, "F")
        self.inputs[-1].default_value = "True"
        self.outputs.new(NLConditionSocket.bl_idname, "If All True")

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

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value_type = "BOOLEAN"
        self.inputs[-1].value = "True"
        self.outputs.new(NLConditionSocket.bl_idname, "When Changed To")

    def get_netlogic_class_name(self):
        return "ULValueChangedTo"

    def get_input_sockets_field_names(self):
        return ["monitored_value", "trigger_value"]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Threshold")
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def update_draw(self):
        numerics = ['INTEGER', 'FLOAT']
        self.inputs[2].enabled = (
            (self.inputs[0].value_type in numerics or self.inputs[0].is_linked)
            and
            (self.inputs[1].value_type in numerics or self.inputs[1].is_linked)
        )

    def get_netlogic_class_name(self):
        return "ULCompare"

    def get_input_sockets_field_names(self):
        return ["param_a", "param_b", 'threshold']

    def get_attributes(self):
        return [
            ("operator", lambda: f'{self.operator}'),
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLXYZSocket.bl_idname, "")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Threshold")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Compare This")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "To This")
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def get_netlogic_class_name(self):
        return "ULCompareVectors"

    def get_input_sockets_field_names(self):
        return ['all', 'threshold', "param_a", "param_b"]

    def get_output_socket_varnames(self):
        return ['OUT']

    def get_attributes(self):
        return [
            ("operator", lambda: f'{self.operator}'),
        ]


_nodes.append(NLConditionCompareVecs)


class NLConditionDistanceCheck(NLConditionNode):
    bl_idname = "NLConditionDistanceCheck"
    bl_label = "Check Distance"
    nl_category = "Math"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLSocketDistanceCheck.bl_idname, "Check")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "A")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "B")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Dist.")
        self.inputs.new(NLSocketOptionalPositiveFloat.bl_idname, "Hyst.")
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "ULCheckDistance"

    def get_input_sockets_field_names(self):
        return ["operator", "param_a", "param_b", "dist", "hyst"]


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
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        utils.register_inputs(self, NLParameterSocket, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If Changed")
        self.outputs.new(NLParameterSocket.bl_idname, "Old Value")
        self.outputs.new(NLParameterSocket.bl_idname, "New Value")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "initialize",
            text="Startup" if self.initialize else "Skip Startup",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "ULOnValueChanged"

    def get_input_sockets_field_names(self):
        return ["current_value"]

    def get_attributes(self):
        return [("initialize", lambda: "True" if self.initialize else "False")]

    def get_output_socket_varnames(self):
        return ['OUT', "OLD", "NEW"]


_nodes.append(NLConditionValueChanged)


class NLConditionTimeElapsed(NLConditionNode):
    bl_idname = "NLConditionTimeElapsed"
    bl_label = "Timer"
    nl_category = 'Time'
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Set Timer")
        self.inputs.new(NLTimeSocket.bl_idname, "Seconds")
        self.outputs.new(NLConditionSocket.bl_idname, "When Elapsed")

    def get_netlogic_class_name(self):
        return "ULTimer"

    def get_input_sockets_field_names(self):
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

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If None")

    def get_netlogic_class_name(self):
        return "ULNone"

    def get_input_sockets_field_names(self):
        return ["checked_value"]


_nodes.append(NLConditionNoneNode)


class NLConditionValueValidNode(NLConditionNode):
    bl_idname = "NLConditionValueValidNode"
    bl_label = "Value Valid"
    nl_category = "Values"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If Valid")

    def get_netlogic_class_name(self):
        return "ULValueValid"

    def get_input_sockets_field_names(self):
        return ["checked_value"]


_nodes.append(NLConditionValueValidNode)


class NLConditionNotNode(NLConditionNode):
    bl_idname = "NLConditionNotNode"
    bl_label = "Not"
    nl_category = "Logic"
    nl_module = 'conditions'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, "If Not")

    def get_netlogic_class_name(self):
        return "ULNot"

    def get_input_sockets_field_names(self):
        return ["condition"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.outputs.new(NLConditionSocket.bl_idname, "If Running")
        self.outputs.new(NLConditionSocket.bl_idname, "If Stopped")

    def get_netlogic_class_name(self):
        return "ULLogicTreeStatus"

    def get_input_sockets_field_names(self):
        return ["game_object", "tree_name"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "Object to Add")
        self.inputs.new(
            NLGameObjectSocket.bl_idname,
            "Copy Data From (Optional)"
        )
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Life")
        self.inputs.new(NLBooleanSocket.bl_idname, "Full Copy")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Added Object")

    def get_netlogic_class_name(self):
        return "ULAddObject"

    def get_input_sockets_field_names(self):
        return ["condition", "name", 'reference', "life", 'full_copy']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Create Pool")
        self.inputs.new(NLConditionSocket.bl_idname, "Spawn")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Spawner")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "Object Instance")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Amount")
        self.inputs[-1].value = 10
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Life")
        self.inputs[-1].value = 3
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Speed")
        self.inputs[-1].value = 75.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Visualize")
        self.outputs.new(NLConditionSocket.bl_idname, "Pool Created")
        self.outputs.new(NLConditionSocket.bl_idname, "Spawned")
        self.outputs.new(NLConditionSocket.bl_idname, "On Hit")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Hit Object")
        self.outputs.new(NLVectorSocket.bl_idname, "Hit Point")
        self.outputs.new(NLVectorSocket.bl_idname, "Hit Normal")
        self.outputs.new(NLVectorSocket.bl_idname, "Hit Direction")

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Start")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "IP")
        self.inputs[-1].value = socket.gethostbyname(socket.gethostname())
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Port")
        self.inputs[-1].value = 8303
        self.inputs.new(NLConditionSocket.bl_idname, "Stop")
        self.outputs.new(NLConditionSocket.bl_idname, "Started")
        self.outputs.new(NLConditionSocket.bl_idname, "Running")
        self.outputs.new(NLConditionSocket.bl_idname, "Stopped")
        self.outputs.new(NLParameterSocket.bl_idname, "Server")
        self.outputs.new(NLConditionSocket.bl_idname, "Received")
        self.outputs.new(NLDictSocket.bl_idname, "Message")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    def get_netlogic_class_name(self):
        return "ULLocalServer"

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Connect")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "IP")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Port")
        self.inputs[-1].value = 8303
        self.inputs.new(NLConditionSocket.bl_idname, "Disconnect")
        self.outputs.new(NLConditionSocket.bl_idname, "Connect")
        self.outputs.new(NLConditionSocket.bl_idname, "Connected")
        self.outputs.new(NLConditionSocket.bl_idname, "Disconnect")
        self.outputs.new(NLParameterSocket.bl_idname, "Client")
        self.outputs.new(NLConditionSocket.bl_idname, "Received")
        self.outputs.new(NLDictSocket.bl_idname, "Message")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    def get_netlogic_class_name(self):
        return "ULLocalClient"

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Server / Client")
        self.inputs.new(NLParameterSocket.bl_idname, "Data")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Subject")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULSendNetworkMessage"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "entity",
            'data',
            'subject'
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULSetProperty"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGeomNodeTreeSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Value')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLNodeGroupSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Value')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGeomNodeTreeSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLNodeGroupSocket.bl_idname, 'Tree')
        self.inputs.new(NLNodeGroupNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLCountSocket.bl_idname, "Slot")
        self.inputs.new(NLMaterialSocket.bl_idname, "Material")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULSetMaterial"

    def update_draw(self):
        obj_socket = self.inputs[1]
        if obj_socket.use_owner or not obj_socket.value:
            return
        if self.inputs[2].value > len(obj_socket.value.material_slots):
            self.inputs[2].value = len(obj_socket.value.material_slots)

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "slot",
            "mat_name",
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Input")
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Value')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Internal")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLTreeNodeSocket.bl_idname, 'Node Name')
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLPlayActionModeSocket.bl_idname, "Mode")
        self.inputs[-1].enabled = False
        self.inputs.new(NLBooleanSocket.bl_idname, 'Continue')
        self.inputs[-1].enabled = False
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Frames")
        self.inputs[-1].enabled = False
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "FPS")
        self.inputs[-1].value = 60
        self.inputs[-1].enabled = False
        self.outputs.new(NLConditionSocket.bl_idname, "On Start")
        self.outputs.new(NLConditionSocket.bl_idname, "Running")
        self.outputs.new(NLConditionSocket.bl_idname, "On Finish")
        self.outputs.new(NLParameterSocket.bl_idname, "Current Frame")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'play_mode',
            'play_continue',
            "frames",
            'fps'
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULToggleProperty"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Range")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

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

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value",
            'range'
        ]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Copy From")
        self.inputs.new(NLGameObjectSocket.bl_idname, "To")
        self.inputs.new(NLGamePropertySocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULCopyProperty"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "from_object",
            "to_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLCopyPropertyFromObject)


class NLValueSwitch(NLParameterNode):
    bl_idname = "NLValueSwitch"
    bl_label = "Value Switch"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "A if True, else B")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = 'A'
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = 'B'
        self.outputs.new(NLParameterSocket.bl_idname, "A or B")

    def get_netlogic_class_name(self):
        return "ULValueSwitch"

    def get_input_sockets_field_names(self):
        return ["condition", 'val_a', 'val_b']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLBooleanSocket.bl_idname, "if A")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "A"
        self.inputs.new(NLBooleanSocket.bl_idname, "elif B")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "B"
        self.inputs.new(NLBooleanSocket.bl_idname, "elif C")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "C"
        self.inputs.new(NLBooleanSocket.bl_idname, "elif D")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "D"
        self.inputs.new(NLBooleanSocket.bl_idname, "elif E")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "E"
        self.inputs.new(NLBooleanSocket.bl_idname, "elif F")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "F"
        self.outputs.new(NLParameterSocket.bl_idname,
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

    def get_input_sockets_field_names(self):
        return [
            "ca", 'val_a',
            "cb", 'val_b',
            "cc", 'val_c',
            "cd", 'val_d',
            "ce", 'val_e',
            "cf", 'val_f'
        ]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLValueFieldSocket.bl_idname, "Switch:")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Default")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case A")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case B")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case C")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case D")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case E")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "Case F")
        self.inputs[-1].value = "_None_"
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = "_None_"
        self.outputs.new(
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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ['RESULT']


_nodes.append(NLValueSwitchListCompare)


class NLInvertValueNode(NLParameterNode):
    bl_idname = "NLInvertValueNode"
    bl_label = "Invert"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULInvertValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLInvertValueNode)


class NLAbsoluteValue(NLParameterNode):
    bl_idname = "NLAbsoluteValue"
    bl_label = "Absolute"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "ULAbsoluteValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Collider")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Suspension")
        self.inputs[-1].value = 0.06
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Stiffness")
        self.inputs[-1].value = 50
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Damping")
        self.inputs[-1].value = 5
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Friction")
        self.inputs[-1].value = 2
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Wheel Modifier")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Vehicle Constraint')
        self.outputs.new(NLListSocket.bl_idname, 'Wheels')

    def get_output_socket_varnames(self):
        return ["OUT", 'VEHICLE', 'WHEELS']

    def get_netlogic_class_name(self):
        return "ULCreateVehicle"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Vehicle")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Power")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplyForce"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Vehicle")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Power")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplyBraking"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Vehicle")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Steer")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleApplySteering"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Collider")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLBooleanSocket.bl_idname, "Suspension")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Stiffness")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Damping")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Friction")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = self.value_type != 'ALL'
        ipts = self.inputs
        ipts[4].enabled = ipts[3].value
        ipts[6].enabled = ipts[5].value
        ipts[8].enabled = ipts[7].value
        ipts[10].enabled = ipts[9].value

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULVehicleSetAttributes"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code,
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLXYZSocket.bl_idname, "")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULSetGameObjectAttribue"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code,
        default='worldPosition'
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.inputs[-1].value = .1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "ULSlowFollow"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Origin")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Aim")
        self.inputs.new(NLBooleanSocket.bl_idname, "Local")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLMaterialSocket.bl_idname, "Material")
        self.inputs.new(NLBooleanSocket.bl_idname, "Exclude")
        self.inputs.new(NLBooleanSocket.bl_idname, 'X-Ray')
        self.inputs.new(NLBooleanSocket.bl_idname, "Custom Distance")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Distance")
        self.inputs[-1].value = 100.0
        self.inputs.new(NLBooleanSocket.bl_idname, 'Visualize')
        self.outputs.new(NLConditionSocket.bl_idname, "Has Result")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Picked Object")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Point")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Normal")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Ray Direction")
        self.outputs.new(NLParameterSocket.bl_idname, "Face Material Name")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "UV Coords")

    def update_draw(self):
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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", "DIRECTION", "MATERIAL", "UV"]


_nodes.append(NLActionRayCastNode)


class NLProjectileRayCast(NLActionNode):
    bl_idname = "NLProjectileRayCast"
    bl_label = "Projectile Ray"
    nl_category = "Ray Casts"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Origin")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Aim")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Local')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Power")
        self.inputs[-1].value = 10.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Distance")
        self.inputs[-1].value = 20.0
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Resolution")
        self.inputs[-1].value = 0.9
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLBooleanSocket.bl_idname, 'X-Ray')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Visualize')
        self.outputs.new(NLConditionSocket.bl_idname, "Has Result")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Picked Object")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Point")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Normal")
        self.outputs.new(NLListSocket.bl_idname, "Parabola")

    def get_netlogic_class_name(self):
        return "ULProjectileRayCast"

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return [OUTCELL, "PICKED_OBJECT", "POINT", "NORMAL", 'PARABOLA']


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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLSocketLogicTree.bl_idname, 'Tree Name')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStartSubNetwork"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLSocketLogicTree.bl_idname, 'Tree Name')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStopSubNetwork"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Visible")
        socket = self.inputs[-1]
        socket.use_toggle = True
        socket.true_label = "Visible"
        socket.false_label = "Not Visibile"
        self.inputs.new(NLBooleanSocket.bl_idname, "Include Children")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetVisibility"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLCollectionSocket.bl_idname, "Collection")
        self.inputs.new(NLBooleanSocket.bl_idname, "Visible")
        socket = self.inputs[-1]
        socket.use_toggle = True
        socket.true_label = "Visible"
        socket.false_label = "Not Visibile"
        self.inputs.new(NLBooleanSocket.bl_idname, "Include Children")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollectionVisibility"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLCurveObjectSocket.bl_idname, "Curve")
        self.inputs.new(NLListSocket.bl_idname, "Points")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCurvePoints"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Object")

    def get_netlogic_class_name(self):
        return "ULGetObject"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "From")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "To")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Subject")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Body")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "ULSendMessage"

    def get_input_sockets_field_names(self):
        return ['condition', 'from_obj', 'to_obj', 'subject', 'body']

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLActionSendMessage)


class NLActionSetActiveCamera(NLActionNode):
    bl_idname = "NLActionSetActiveCamera"
    bl_label = "Set Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Camera')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCamera"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Camera')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'FOV')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCameraFOV"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Camera')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Scale')
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCameraOrthoScale"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", 'scale']


_nodes.append(NLActionSetCameraOrthoScale)


class NLActionSetResolution(NLActionNode):
    bl_idname = "NLActionSetResolution"
    bl_label = "Set Resolution"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'X')
        self.inputs[-1].value = 1920
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'Y')
        self.inputs[-1].value = 1080
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetResolution"

    def get_input_sockets_field_names(self):
        return ["condition", "x_res", 'y_res']


_nodes.append(NLActionSetResolution)


class NLActionSetFullscreen(NLActionNode):
    bl_idname = "NLActionSetFullscreen"
    bl_label = "Set Fullscreen"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Fullscreen')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetFullscreen"

    def get_input_sockets_field_names(self):
        return ["condition", "use_fullscreen"]


_nodes.append(NLActionSetFullscreen)


class NLSetProfile(NLActionNode):
    bl_idname = "NLSetProfile"
    bl_label = "Show Profile"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Show')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetProfile"

    def get_input_sockets_field_names(self):
        return ["condition", "use_profile"]


_nodes.append(NLSetProfile)


class NLShowFramerate(NLActionNode):
    bl_idname = "NLShowFramerate"
    bl_label = "Show Framerate"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Show')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULShowFramerate"

    def get_input_sockets_field_names(self):
        return ["condition", "use_framerate"]


_nodes.append(NLShowFramerate)


class NLActionSetVSync(NLActionNode):
    bl_idname = "NLActionSetVSync"
    bl_label = "Set VSync"
    nl_category = 'Render'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLVSyncSocket.bl_idname, 'Vsync')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetVSync"

    def get_input_sockets_field_names(self):
        return ["condition", "vsync_mode"]


_nodes.append(NLActionSetVSync)


class NLInitEmptyDict(NLParameterNode):
    bl_idname = "NLInitEmptyDict"
    bl_label = "Create Empty"
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Key')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
        return ['DICT']

    def get_netlogic_class_name(self):
        return "ULInitNewDict"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLDictSocket.bl_idname, 'Dictionary')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Key')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
        return ["OUT", "DICT"]

    def get_netlogic_class_name(self):
        return "ULSetDictKey"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLDictSocket.bl_idname, 'Dictionary')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Key')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')
        self.outputs.new(NLParameterSocket.bl_idname, 'Value')

    def get_output_socket_varnames(self):
        return ["OUT", "DICT", 'VALUE']

    def get_netlogic_class_name(self):
        return "ULPopDictKey"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'Length')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ['LIST']

    def get_netlogic_class_name(self):
        return "ULInitEmptyList"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLListItemSocket.bl_idname, 'Item')
        self.inputs.new(NLListItemSocket.bl_idname, 'Item')
        self.outputs.new(NLListSocket.bl_idname, 'List')

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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLListSocket.bl_idname, 'List 1')
        self.inputs.new(NLListSocket.bl_idname, 'List 2')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULExtendList"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLListSocket.bl_idname, 'List')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULAppendListItem"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLListSocket.bl_idname, 'List')
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'Index')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULSetListIndex"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLListSocket.bl_idname, 'List')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULRemoveListValue"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLListSocket.bl_idname, 'List')
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'Index')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", "LIST"]

    def get_netlogic_class_name(self):
        return "ULRemoveListIndex"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.inputs.new(NLBooleanSocket.bl_idname, "Initialize")
        self.inputs[-1].use_toggle = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULInstallSubNetwork"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULExecuteSubNetwork"

    def get_input_sockets_field_names(self):
        return ["condition", "target_object", "tree_name"]


_nodes.append(NLActionExecuteNetwork)


class NLActionStopAnimation(NLActionNode):
    bl_idname = "NLActionStopAnimation"
    bl_label = "Stop Animation"
    nl_category = "Animation"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(
            NLPositiveIntegerFieldSocket.bl_idname,
            "Animation Layer"
        )
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULStopAction"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "action_layer"]


_nodes.append(NLActionStopAnimation)


class NLActionSetAnimationFrame(NLActionNode):
    bl_idname = "NLActionSetAnimationFrame"
    bl_label = "Set Animation Frame"
    nl_category = "Animation"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLAnimationSocket.bl_idname, "Action")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Frame")
        self.inputs.new(NLBooleanSocket.bl_idname, "Freeze")
        self.inputs[-1].value = True
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Layer Weight")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetActionFrame"

    def get_input_sockets_field_names(self):
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
    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3RotationSocket, "Vector")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector"
        )
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
    local: BoolProperty(default=False, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Point')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Direction')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Main Object')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Head Object (Optional)')
        self.inputs.new(NLInvertedXYSocket.bl_idname, 'Inverted')
        self.inputs[-1].x = True
        self.inputs.new(NLPositiveIntCentSocket.bl_idname, 'Index')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Sensitivity')
        self.inputs[-1].value = .25
        self.inputs.new(NLPositiveStepFloat.bl_idname, 'Exponent')
        self.inputs[-1].value = 2.3
        self.inputs.new(NLBooleanSocket.bl_idname, 'Cap Left / Right')
        self.inputs.new(NLAngleLimitSocket.bl_idname, '')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Cap Up / Down')
        self.inputs.new(NLAngleLimitSocket.bl_idname, '')
        self.inputs[-1].value_x = math.radians(89)
        self.inputs[-1].value_y = math.radians(89)
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Threshold')
        self.inputs[-1].value = 0.1
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def update_draw(self):
        ipts = self.inputs
        ipts[8].enabled = ipts[7].value
        ipts[10].enabled = ipts[9].value

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadLook"

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.outputs.new(NLParameterSocket.bl_idname, 'Layout')
        self.outputs.new(NLListSocket.bl_idname, 'Widgets')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULUILayout"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object"]


# _nodes.append(NLUILayout)


class NLSetCollisionGroup(NLActionNode):
    bl_idname = "NLSetCollisionGroup"
    bl_label = "Set Collision Group"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLCollisionMaskSocket.bl_idname, 'Group')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollisionGroup"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'slots']


_nodes.append(NLSetCollisionGroup)


class NLSetCollisionMask(NLActionNode):
    bl_idname = "NLSetCollisionMask"
    bl_label = "Set Collision Mask"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLCollisionMaskSocket.bl_idname, 'Mask')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCollisionMask"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULCharacterJump"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Force')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterJumpSpeed"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "force"]


_nodes.append(NLSetCharacterJumpSpeed)


class NLActionSaveGame(NLActionNode):
    bl_idname = "NLActionSaveGame"
    bl_label = "Save Game"
    bl_icon = 'FILE_TICK'
    nl_category = "Game"
    nl_module = 'actions'
    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, 'Slot')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionSaveGame)


class NLActionLoadGame(NLActionNode):
    bl_idname = "NLActionLoadGame"
    bl_label = "Load Game"
    bl_icon = 'FILE_FOLDER'
    nl_category = "Game"
    nl_module = 'actions'
    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, 'Slot')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionLoadGame)


class NLActionSaveVariable(NLActionNode):
    bl_idname = "NLActionSaveVariable"
    bl_label = "Save Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Variable')
        self.inputs[-1].value = 'var'
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionSaveVariable)


class NLActionSaveVariables(NLActionNode):
    bl_idname = "NLActionSaveVariables"
    bl_label = "Save Variable Dict"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.inputs.new(NLDictSocket.bl_idname, 'Variables')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionSaveVariables)


class NLSetScene(NLActionNode):
    bl_idname = "NLSetScene"
    bl_label = "Set Scene"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLSceneSocket.bl_idname, "Scene")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_netlogic_class_name(self):
        return "ULSetScene"

    def get_input_sockets_field_names(self):
        return ['condition', 'scene']

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLSetScene)


class NLLoadScene(NLActionNode):
    bl_idname = "NLLoadScene"
    bl_label = "Load Scene"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLSceneSocket.bl_idname, "Scene")
        self.outputs.new(NLConditionSocket.bl_idname, 'Loaded')
        self.outputs.new(NLConditionSocket.bl_idname, 'Updated')
        self.outputs.new(NLParameterSocket.bl_idname, 'Status')
        self.outputs.new(NLParameterSocket.bl_idname, 'Datatype')
        self.outputs.new(NLParameterSocket.bl_idname, 'Item')

    def get_netlogic_class_name(self):
        return "ULLoadScene"

    def get_input_sockets_field_names(self):
        return ['condition', 'scene']

    def get_output_socket_varnames(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']


_nodes.append(NLLoadScene)


class NLLoadFileContent(NLActionNode):
    bl_idname = "NLLoadFileContent"
    bl_label = "Load File Content"
    nl_category = "File"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.outputs.new(NLConditionSocket.bl_idname, 'Loaded')
        self.outputs.new(NLConditionSocket.bl_idname, 'Updated')
        self.outputs.new(NLParameterSocket.bl_idname, 'Status')
        self.outputs.new(NLParameterSocket.bl_idname, 'Datatype')
        self.outputs.new(NLParameterSocket.bl_idname, 'Item')

    def get_netlogic_class_name(self):
        return "ULLoadFileContent"

    def get_input_sockets_field_names(self):
        return ['condition']

    def get_output_socket_varnames(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']


_nodes.append(NLLoadFileContent)


class NLParameterSetAttribute(NLActionNode):
    bl_idname = "NLParameterSetAttribute"
    bl_label = "Set Object Attribute"
    nl_category = "Python"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPythonSocket.bl_idname, "Object Instance")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")

    def get_netlogic_class_name(self):
        return "ULSetPyInstanceAttr"

    def get_input_sockets_field_names(self):
        return ['condition', 'instance', 'attr', 'value']


_nodes.append(NLParameterSetAttribute)


class NLActionLoadVariable(NLActionNode):
    bl_idname = "NLActionLoadVariable"
    bl_label = "Load Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'parameters'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'var'
        self.inputs.new(NLOptionalValueFieldSocket.bl_idname, 'Default Value')
        self.outputs.new(NLParameterSocket.bl_idname, 'Value')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ['VAR']


_nodes.append(NLActionLoadVariable)


class NLActionLoadVariables(NLActionNode):
    bl_idname = "NLActionLoadVariables"
    bl_label = "Load Variable Dict"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'parameters'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.outputs.new(NLDictSocket.bl_idname, 'Variables')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["VAR"]


_nodes.append(NLActionLoadVariables)


class NLActionRemoveVariable(NLActionNode):
    bl_idname = "NLActionRemoveVariable"
    bl_label = "Remove Variable"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'var'
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionRemoveVariable)


class NLActionClearVariables(NLActionNode):
    bl_idname = "NLActionClearVariables"
    bl_label = "Clear Variables"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLActionClearVariables)


class NLActionListVariables(NLActionNode):
    bl_idname = "NLActionListVariables"
    bl_label = "List Saved Variables"
    nl_category = "Data"
    nl_subcat = "Variables"
    nl_module = 'actions'

    custom_path: BoolProperty(update=update_tree_code)
    path: StringProperty(
        subtype='DIR_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Filename')
        self.inputs[-1].value = 'variables'
        self.inputs.new(NLBooleanSocket.bl_idname, 'Print')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Max Jumps")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterMaxJumps"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'max_jumps']


_nodes.append(NLActionSetCharacterJump)


class NLActionSetCharacterGravity(NLActionNode):
    bl_idname = "NLActionSetCharacterGravity"
    bl_label = "Set Gravity"
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVelocitySocket.bl_idname, "Gravity")
        self.inputs[-1].value_z = -9.8
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCharacterGravity"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'gravity']


_nodes.append(NLActionSetCharacterGravity)


class NLActionSetCharacterWalkDir(NLActionNode):
    bl_idname = "NLActionSetCharacterWalkDir"
    bl_label = "Walk"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'actions'

    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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

    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Velocity")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Time")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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

    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        utils.register_inputs(
            self,
            NLConditionSocket, "Condition",
            NLGameObjectSocket, "Object",
            NLVec3FieldSocket, "Vector")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
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

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULEndObject"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object"]


_nodes.append(NLActionEndObjectNode)


class NLActionSetTimeScale(NLActionNode):
    bl_idname = "NLActionSetTimeScale"
    bl_label = "Set Timescale"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Timescale")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetTimeScale"

    def get_input_sockets_field_names(self):
        return ["condition", "timescale"]


_nodes.append(NLActionSetTimeScale)


class NLActionSetGravity(NLActionNode):
    bl_idname = "NLActionSetGravity"
    bl_label = "Set Gravity"
    nl_category = "Scene"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLVelocitySocket.bl_idname, "Gravity")
        self.inputs[-1].value_z = -9.8
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetGravity"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLMeshSocket.bl_idname, "New Mesh Name")
        self.inputs.new(NLBooleanSocket.bl_idname, "Use Display")
        self.inputs.new(NLBooleanSocket.bl_idname, "Use Physics")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULReplaceMesh"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRemovePhysicsConstraint"

    def get_input_sockets_field_names(self):
        return ["condition", "object", "name"]


_nodes.append(NLActionRemovePhysicsConstraint)


class NLActionAddPhysicsConstraint(NLActionNode):
    bl_idname = "NLActionAddPhysicsConstraint"
    bl_label = "Add Constraint"
    bl_icon = 'CONSTRAINT'
    nl_category = "Physics"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs.new(NLConstraintTypeSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use World Space')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Pivot')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Limit Axis')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Axis Limits')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Linked Collision')
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        state = self.inputs[4].value
        if state == 'bge.constraints.POINTTOPOINT_CONSTRAINT':
            self.inputs[7].enabled = False
            self.inputs[8].enabled = False
            return
        else:
            self.inputs[7].enabled = True
        if not self.inputs[7].value:
            self.inputs[8].enabled = False
        else:
            self.inputs[8].enabled = True

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULAddPhysicsConstraint"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "target",
            "child",
            "name",
            "constraint",
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Gamma')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetGamma"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Exposure')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetExposure"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use AO')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeAO"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Bloom')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeBloom"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use SSR')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSSR"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Volumetrics')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeVolumetrics"

    def get_input_sockets_field_names(self):
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

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use SMAA')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSMAA"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeSMAA)


class NLSetEeveeSMAAQuality(NLActionNode):
    bl_idname = "NLSetEeveeSMAAQuality"
    bl_label = "Set SMAA Quality"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQualitySocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSMAAQuality"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


_nodes.append(NLSetEeveeSMAAQuality)


class NLSetLightEnergyAction(NLActionNode):
    bl_idname = "NLSetLightEnergyAction"
    bl_label = "Set Light Energy"
    nl_category = "Lights"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLLightObjectSocket.bl_idname, 'Light Object')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Energy')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightEnergy"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLLightObjectSocket.bl_idname, 'Light Object')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLLightObjectSocket.bl_idname, 'Light')

    def get_output_socket_varnames(self):
        return ["OUT", 'LIGHT']

    def get_netlogic_class_name(self):
        return "ULMakeUniqueLight"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLLightObjectSocket.bl_idname, 'Light Object')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Shadow')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightShadow"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLLightObjectSocket.bl_idname, "Light Object")
        self.inputs.new(NLColorSocket.bl_idname, "Color")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetLightColor"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLLightObjectSocket.bl_idname, "Light Object")
        self.outputs.new(NLParameterSocket.bl_idname, 'Enery')

    def get_output_socket_varnames(self):
        return ['ENERGY']

    def get_netlogic_class_name(self):
        return "ULGetLightEnergy"

    def get_input_sockets_field_names(self):
        return ["lamp"]


_nodes.append(NLGetLightEnergy)


class NLGetLightColorAction(NLParameterNode):
    bl_idname = "NLGetLightColorAction"
    bl_label = "Get Light Color"
    nl_category = "Lights"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLLightObjectSocket.bl_idname, "Light Object")
        self.outputs.new(NLColorSocket.bl_idname, 'Color')

    def get_output_socket_varnames(self):
        return ['COLOR']

    def get_netlogic_class_name(self):
        return "ULGetLightColor"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object / Armature")
        self.inputs.new(NLAnimationSocket.bl_idname, "Action")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Start")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "End")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Priority")
        self.inputs[-1].enabled = False
        self.inputs.new(NLPlayActionModeSocket.bl_idname, "Play Mode")
        self.inputs.new(NLBooleanSocket.bl_idname, "Stop When Done")
        self.inputs[-1].value = True
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Layer Weight")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Blendin")
        self.inputs.new(NLBlendActionModeSocket.bl_idname, "Blend Mode")
        self.outputs.new(NLConditionSocket.bl_idname, "Started")
        self.outputs.new(NLConditionSocket.bl_idname, "Running")
        self.outputs.new(NLConditionSocket.bl_idname, "On Finish")
        self.outputs.new(NLParameterSocket.bl_idname, "Current Frame")

    def update_draw(self):
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

    def get_input_sockets_field_names(self):
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

    def get_output_socket_varnames(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]


_nodes.append(NLActionPlayActionNode)


class NLActionAlignAxisToVector(NLActionNode):
    bl_idname = "NLActionAlignAxisToVector"
    bl_label = "Align Axis to Vector"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'
    local: BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Axis")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "local",
            toggle=True,
            text="Local" if self.local else "Global"
        )

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULAlignAxisToVector"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLTimeSocket.bl_idname, 'Time')
        self.outputs.new(NLConditionSocket.bl_idname, 'Out')

    def get_netlogic_class_name(self):
        return 'ULBarrier'

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLTimeSocket.bl_idname, 'Delay')
        self.outputs.new(NLConditionSocket.bl_idname, 'Out')

    def get_netlogic_class_name(self):
        return 'ULTimeDelay'

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLTimeSocket.bl_idname, "Gap")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "ULPulsify"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code,
        default="1"
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Main Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Head (Optional)")
        self.inputs.new(NLInvertedXYSocket.bl_idname, "")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Sensitivity")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Cap Left / Right")
        self.inputs.new(NLAngleLimitSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Cap Up / Down")
        self.inputs.new(NLAngleLimitSocket.bl_idname, "")
        self.inputs[-1].value_x = math.radians(-89)
        self.inputs[-1].value_y = math.radians(89)
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Smoothing")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        r = layout.row(align=True)
        r.label(text="Front:")
        r.prop(self, "axis", text="")

    def update_draw(self):
        if self.inputs[5].value:
            self.inputs[6].enabled = True
        else:
            self.inputs[6].enabled = False
        if self.inputs[7].value:
            self.inputs[8].enabled = True
        else:
            self.inputs[8].enabled = False

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULMouseLook"

    def get_attributes(self):
        return [("axis", lambda: self.axis)]

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'msg_type', text='')

    def get_attributes(self):
        return [("msg_type", lambda: f'"{self.msg_type}"')]

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULPrintValue"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Camera")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLBooleanSocket.bl_idname, 'X-Ray')
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Distance")
        self.inputs[-1].value = 100.0
        self.outputs.new(NLConditionSocket.bl_idname, "Has Result")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Picked Object")
        self.outputs.new(NLVectorSocket.bl_idname, "Picked Point")
        self.outputs.new(NLVectorSocket.bl_idname, "Picked Normal")

    def get_netlogic_class_name(self):
        return "ULMouseRayCast"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", "property", 'xray', "distance"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "OUTOBJECT", "OUTPOINT", "OUTNORMAL"]


_nodes.append(NLActionMousePickNode)


class NLActionCameraPickNode(NLActionNode):
    bl_idname = "NLActionCameraPickNode"
    bl_label = "Camera Ray"
    bl_icon = 'CAMERA_DATA'
    nl_category = "Ray Casts"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Camera")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Aim")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLBooleanSocket.bl_idname, 'X-Ray')
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Distance")
        self.inputs[-1].value = 100.0
        self.outputs.new(NLConditionSocket.bl_idname, "Has Result")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Picked Object")
        self.outputs.new(NLVectorSocket.bl_idname, "Picked Point")
        self.outputs.new(NLVectorSocket.bl_idname, "Picked Normal")

    def get_netlogic_class_name(self):
        return "ULCameraRayCast"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", "aim", "property_name", "xray", "distance"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "PICKED_OBJECT", "PICKED_POINT", "PICKED_NORMAL"]


_nodes.append(NLActionCameraPickNode)


class NLActionSetParentNode(NLActionNode):
    bl_idname = "NLActionSetParentNode"
    bl_label = "Set Parent"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Parent Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Compound")
        self.inputs[-1].value = True
        self.inputs[-1].enabled = False
        self.inputs.new(NLBooleanSocket.bl_idname, "Ghost")
        self.inputs[-1].value = True
        self.inputs[-1].enabled = False
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetParent"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRemoveParent"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Print Profile")
        self.inputs.new(NLBooleanSocket.bl_idname, "Evaluated Nodes")
        self.inputs.new(NLBooleanSocket.bl_idname, "Nodes per Second")
        self.inputs.new(NLBooleanSocket.bl_idname, "Nodes per Tick")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Profile')

    def get_output_socket_varnames(self):
        return ["OUT", "DATA"]

    def get_netlogic_class_name(self):
        return "ULGetPerformanceProfile"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Parent Object")

    def get_netlogic_class_name(self):
        return "ULGetParent"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'axis', text='')

    def get_netlogic_class_name(self):
        return "ULAxisVector"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("axis", lambda: self.axis)]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLParameterSocket.bl_idname, "Name")

    def get_netlogic_class_name(self):
        return "ULObjectDataName"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLCurveObjectSocket.bl_idname, "Curve")
        self.outputs.new(NLListSocket.bl_idname, "Points")

    def get_netlogic_class_name(self):
        return "ULGetCurvePoints"

    def get_input_sockets_field_names(self):
        return ["curve"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLListSocket.bl_idname, "Vertices")

    def get_netlogic_class_name(self):
        return "ULObjectDataVertices"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLBoneConstraintSocket.bl_idname, "")
        self.inputs[-1].ref_index = 2
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Influence")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = (
            self.inputs[1].value is not None or
            self.inputs[1].is_linked or
            self.inputs[1].use_owner
        )
        self.inputs[3].enabled = (
            self.inputs[2].enabled and
            (self.inputs[2].value != '' or
             self.inputs[2].is_linked)
        )

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintInfluence"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLBoneConstraintSocket.bl_idname, "")
        self.inputs[-1].ref_index = 2
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = (
            self.inputs[1].value is not None or
            self.inputs[1].is_linked or
            self.inputs[1].use_owner
        )
        self.inputs[3].enabled = (
            self.inputs[2].enabled and
            (self.inputs[2].value != '' or
             self.inputs[2].is_linked)
        )

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintTarget"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLBoneConstraintSocket.bl_idname, "")
        self.inputs[-1].ref_index = 2
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = (
            self.inputs[1].value is not None or
            self.inputs[1].is_linked or
            self.inputs[1].use_owner
        )
        self.inputs[3].enabled = (
            self.inputs[2].enabled and
            (self.inputs[2].value != '' or
             self.inputs[2].is_linked)
        )

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBoneConstraintAttribute"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "Bone Name")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Set Pos")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetBonePosition"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLArmatureObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLArmatureBoneSocket.bl_idname, "Bone Name")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Set Pos")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Set Rot")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Set Scale")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Translate")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Rotate")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Scale")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULEditBone"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Active")
        self.inputs.new(NLBooleanSocket.bl_idname, "Ghost")
        self.inputs[-1].value = False
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetDynamics"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Active")
        self.inputs.new(NLBooleanSocket.bl_idname, "Cut Constraints")
        self.inputs[-1].value = False
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetPhysics"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Enabled")
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetRigidBody"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen X")
        self.inputs[-1].value = 0.5
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen Y")
        self.inputs[-1].value = 0.5
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetMousePosition"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Visible")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetCursorVisibility"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Speaker")
        self.inputs.new(NLSoundFileSocket.bl_idname, "Sound File")
        self.inputs.new(NLBooleanSocket.bl_idname, "Use Occlusion")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Transition')
        self.inputs[-1].value = .1
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Lowpass')
        self.inputs[-1].value = .1
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Pitch")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Volume")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Enable Reverb")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Attenuation")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Reference Distance")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Cone Inner / Outer")
        self.inputs[-1].value_x = 360
        self.inputs[-1].value_y = 360
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Cone Outer Volume")
        self.inputs[-1].value = 0.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Ignore Timescale")
        self.outputs.new(NLConditionSocket.bl_idname, 'On Start')
        self.outputs.new(NLConditionSocket.bl_idname, 'On Finish')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

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

    def get_output_socket_varnames(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSound3D"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLSpeakerSocket.bl_idname, "Speaker")
        self.inputs.new(NLBooleanSocket.bl_idname, "Use Occlusion")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Transition')
        self.inputs[-1].value = .1
        self.inputs.new(NLSocketAlphaFloat.bl_idname, 'Lowpass')
        self.inputs[-1].value = .1
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLBooleanSocket.bl_idname, "Ignore Timescale")
        self.outputs.new(NLConditionSocket.bl_idname, 'On Start')
        self.outputs.new(NLConditionSocket.bl_idname, 'On Finish')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

    def update_draw(self):
        self.inputs[3].enabled = self.inputs[4].enabled = self.inputs[2].value

    def get_output_socket_varnames(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSpeaker"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLSoundFileSocket.bl_idname, "Sound File")
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Pitch")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Volume")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Ignore Timescale")
        self.outputs.new(NLConditionSocket.bl_idname, 'On Start')
        self.outputs.new(NLConditionSocket.bl_idname, 'On Finish')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

    def get_output_socket_varnames(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_netlogic_class_name(self):
        return "ULStartSound"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_netlogic_class_name(self):
        return "ULStopAllSounds"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Sound")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_netlogic_class_name(self):
        return "ULStopSound"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Sound")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_netlogic_class_name(self):
        return "ULPauseSound"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Sound")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_netlogic_class_name(self):
        return "ULResumeSound"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")

    def get_netlogic_class_name(self):
        return "ULEndGame"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULRestartGame"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLActionRestartGame)


class NLActionStartGame(NLActionNode):
    bl_idname = "NLActionStartGame"
    bl_label = "Load File"
    nl_category = "Game"
    nl_module = 'actions'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFilePathSocket.bl_idname, "File name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULLoadBlendFile"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Subject")
        self.outputs.new(NLConditionSocket.bl_idname, "Received")
        self.outputs.new(NLParameterSocket.bl_idname, "Content")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Messenger")

    def get_input_sockets_field_names(self):
        return ['subject']

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLGlobalCatSocket.bl_idname, "Category")
        self.inputs.new(NLGlobalPropSocket.bl_idname, "Property")
        self.inputs.new(NLOptionalValueFieldSocket.bl_idname, "Default Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def update_draw(self):
        self.inputs[1].enabled = True if self.inputs[0].value or self.inputs[0].is_linked else False

    def get_input_sockets_field_names(self):
        return ["data_id", "key", 'default']

    def get_netlogic_class_name(self):
        return "ULGetGlobalValue"

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGlobalCatSocket.bl_idname, "Category")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Print')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLDictSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ['condition', "data_id", 'print_d']

    def get_output_socket_varnames(self):
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
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Subject")
        self.inputs.new(NLOptionalValueFieldSocket.bl_idname, "Content")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Messenger")
        self.inputs[-1].use_owner = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        adv = [2, 3]
        for x in adv:
            self.inputs[x].enabled = self.advanced

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NodeSocketPseudoCondition.bl_idname, "Condition")
        self.inputs.new(NLGlobalCatSocket.bl_idname, "Category")
        self.inputs.new(NLGlobalPropSocket.bl_idname, "Property")
        self.inputs[-1].ref_index = 1
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Persistent")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def update_draw(self):
        self.inputs[2].enabled = True if self.inputs[1].value or self.inputs[1].is_linked else False
        self.inputs[3].enabled = self.inputs[4].enabled = self.inputs[2].enabled

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Format String")
        self.inputs[-1].formatted = True
        self.inputs[-1].value = "A is {} and B is {}"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "A")
        self.inputs[-1].value = "Hello"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "B")
        self.inputs[-1].value = "World"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "C")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "D")
        self.outputs.new(NLParameterSocket.bl_idname, "String")

    def update_draw(self):
        string = self.inputs[0].value
        count = string.count('{}')
        ipts = [1, 2, 3, 4]
        for ipt in ipts:
            if ipt <= count:
                self.inputs[ipt].enabled = True
            else:
                self.inputs[ipt].enabled = False

    def get_input_sockets_field_names(self):
        return ["format_string", "value_a", "value_b", "value_c", "value_d"]

    def get_netlogic_class_name(self):
        return "ULFormattedString"

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Max")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Min")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "ULRandomInt"

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Max")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Min")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "ULRandomFloat"

    def get_output_socket_varnames(self):
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
        self.inputs.new(NLXYZSocket.bl_idname, "")
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_input_sockets_field_names(self):
        return ['xyz']

    def get_netlogic_class_name(self):
        return "ULRandomVect"

    def get_output_socket_varnames(self):
        return ["OUT_A"]


_nodes.append(NLRandomVect)


class NLParameterDistance(NLParameterNode):
    bl_idname = "NLParameterDistance"
    bl_label = "Distance"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, "A")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "B")
        self.outputs.new(NLParameterSocket.bl_idname, "Distance")

    def get_input_sockets_field_names(self):
        return ["parama", "paramb"]

    def get_netlogic_class_name(self):
        return "ULDistance"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterDistance)


class NLParameterKeyboardKeyCode(NLParameterNode):
    bl_idname = "NLParameterKeyboardKeyCode"
    bl_label = "Key Code"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'parameters'
    value: StringProperty(update=update_tree_code)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLKeyboardKeySocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Code")

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Target Location")
        self.inputs.new(NLBooleanSocket.bl_idname, "Move as Dynamic")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Stop At Distance")
        self.inputs[-1].value = 0.5
        self.outputs.new(NLConditionSocket.bl_idname, "When Done")

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Local")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Speed")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, "When Done")

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Target")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLSocketLocalAxis.bl_idname, "Rot Axis")
        self.inputs[-1].value = '2'

        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Front")
        self.inputs[-1].value = '1'
        self.outputs.new(NLConditionSocket.bl_idname, "When Done")

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Moving Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Rotating Object")
        self.inputs.new(NLNavMeshSocket.bl_idname, "Navmesh Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Destination")
        self.inputs.new(NLBooleanSocket.bl_idname, "Move as Dynamic")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Lin Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Reach Threshold")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Look At")
        self.inputs[-1].value = True
        self.inputs.new(NLSocketLocalAxis.bl_idname, "Rot Axis")
        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Front")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Rot Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Visualize")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLConditionSocket.bl_idname, "When Reached")
        self.outputs.new(NLListSocket.bl_idname, "Next Point")

    def get_output_socket_varnames(self):
        return ["OUT", "FINISHED", "POINT"]

    def get_netlogic_class_name(self):
        return "ULMoveToWithNavmesh"

    def get_input_sockets_field_names(self):
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
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Moving Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Rotating Object")
        self.inputs.new(NLListSocket.bl_idname, "Path Points")
        self.inputs.new(NLBooleanSocket.bl_idname, "Loop")
        self.inputs.new(NLBooleanSocket.bl_idname, "Continue")
        self.inputs.new(NLNavMeshSocket.bl_idname, "Optional Navmesh")
        self.inputs.new(NLBooleanSocket.bl_idname, "Move as Dynamic")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Lin Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Reach Threshold")
        self.inputs[-1].value = .2
        self.inputs.new(NLBooleanSocket.bl_idname, "Look At")
        self.inputs[-1].value = True
        self.inputs.new(NLSocketOptionalPositiveFloat.bl_idname, "Rot Speed")
        self.inputs.new(NLSocketLocalAxis.bl_idname, "Rot Axis")
        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Front")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULFollowPath"

    def get_input_sockets_field_names(self):
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
        update=update_tree_code
    )
    predefined_formulas: EnumProperty(
        name='Operation',
        items=_enum_predefined_math_fun,
        update=on_fun_changed,
        default="User Defined")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "a")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "b")
        self.outputs.new(NLParameterSocket.bl_idname, "Result")
        self.value = "a + b"

    def draw_buttons(self, context, layout):
        layout.prop(self, "predefined_formulas", text="Predef.")
        if self.predefined_formulas == 'User Defined':
            layout.prop(self, "value", text="Formula")

    def get_input_sockets_field_names(self):
        return ["a", "b"]

    def get_attributes(self):
        return [("formula", '"{0}"'.format(self.value))]

    def get_netlogic_class_name(self):
        return "ULFormula"

    def get_output_socket_varnames(self):
        return ["OUT"]


_nodes.append(NLParameterMathFun)
