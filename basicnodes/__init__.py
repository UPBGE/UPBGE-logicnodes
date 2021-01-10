import re
import bpy
import bge_netlogic
from bge_netlogic import utilities as tools

TOO_OLD = bpy.app.version < (2, 80, 0)

CONDITION_SOCKET_COLOR = tools.Color.RGBA(.8, 0.2, 0.2, 1.0)
PSEUDO_COND_SOCKET_COLOR = tools.Color.RGBA(.8, 0.2, 0.2, 1.0)
PARAMETER_SOCKET_COLOR = tools.Color.RGBA(.8, 0.5, 0.2, 1.0)
PARAM_LIST_SOCKET_COLOR = tools.Color.RGBA(0.74, .65, .48, 1.0)
PARAM_DICT_SOCKET_COLOR = tools.Color.RGBA(0.58, 0.48, .74, 1.0)
PARAM_OBJ_SOCKET_COLOR = tools.Color.RGBA(0.2, 0.5, .7, 1.0)
PARAM_MAT_SOCKET_COLOR = tools.Color.RGBA(.75, .35, .37, 1.0)
PARAM_MESH_SOCKET_COLOR = tools.Color.RGBA(.0, .65, .35, 1.0)
PARAM_COLL_SOCKET_COLOR = tools.Color.RGBA(0.25, 0.35, .8, 1.0)
PARAM_SCENE_SOCKET_COLOR = tools.Color.RGBA(0.5, 0.5, 0.6, 1.0)
PARAM_VECTOR_SOCKET_COLOR = tools.Color.RGBA(0.4, 0.8, 0.4, 1.0)
PARAM_SOUND_SOCKET_COLOR = tools.Color.RGBA(0.2, 0.5, 0.2, 1.0)
PARAM_LOGIC_BRICK_SOCKET_COLOR = tools.Color.RGBA(0.9, 0.9, 0.4, 1.0)
PARAM_PYTHON_SOCKET_COLOR = tools.Color.RGBA(0.2, 0.7, 1, 1.0)
ACTION_SOCKET_COLOR = tools.Color.RGBA(0.2, .7, .7, 1.0)

CONDITION_NODE_COLOR = tools.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = tools.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = tools.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = tools.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]

_sockets = []
_nodes = []


_enum_local_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "Z Axis", "The Local Z Axis [Integer Value 2]")
]

_enum_local_oriented_axis = [
    ("0", "+X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "+Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "+Z Axis", "The Local Z Axis [Integer Value 2]"),
    ("3", "-X Axis", "The Local X Axis [Integer Value 3]"),
    ("4", "-Y Axis", "The Local Y Axis [Integer Value 4]"),
    ("5", "-Z Axis", "The Local Z Axis [Integer Value 5]")
]

_enum_value_filters_3 = [
    ("1", "Range Constraint", "Limit A between B and C [1]")
]


_enum_mouse_wheel_direction = [
    ("1", "Scroll Up", "Mouse Wheel Scrolled Up [1]"),
    ("2", "Scroll Down", "Mouse Wheel Scrolled Down [2]"),
    ("3", "Scroll Up or Down", "Mouse Wheel Scrolled either Up or Down[3]")
]


_enum_vector_math_options = [
    ("normalize", "Normalize", "Rescale all values to 0 - 1"),
    ("lerp", "Lerp", "Liner Interpolation between the two vectors"),
    ("negate", "Negate", "Multiply all values by -1"),
    ("dot", "Dot Product", "Return the dot product of the vectors"),
    ("cross", "Cross Product", "Return the cross product of the vectors"),
    ("project", "Project", "Project this vector onto another")
]


_enum_type_casts = [
    ("int", "To Integer", "Convert this value to an integer type"),
    ("bool", "To Boolean", "Convert this value to a boolean type"),
    ("str", "To String", "Convert this value to a string type"),
    ("float", "To Float", "Convert this value to a float type")
]


_enum_distance_models = {
    ('INVERSE', 'Inverse', ''),
    ('INVERSE_CLAMPED', 'Inverse Clamped', ''),
    ('EXPONENT', 'Exponent', ''),
    ('EXPONENT_CLAMPED', 'Exponent Clamped', ''),
    ('LINEAR', 'Linear', ''),
    ('LINEAR_CLAMPED', 'Linear Clamped', ''),
    ('NONE', 'None', "Don't use a distance model")
}


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
_enum_boolean_values = [
    ("True", "TRUE", "The True value"),
    ("False", "FALSE", "The False value")
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

_enum_optional_positive_float_value_types = [
    ("NONE", "None", "No value"),
    ("FLOAT", "Float", "A positive decimal value")
]

_enum_add_scene_types = [
    ("1", "Overlay", "Draw on top of the 3D environment"),
    ("0", "Underlay", "Draw as background of the 3D environment")
]

_enum_mouse_motion = [
    ("UP", "Mouse Up", "Mouse moves up"),
    ("DOWN", "Mouse Down", "Mouse moves down"),
    ("LEFT", "Mouse Left", "Mouse moves left"),
    ("RIGHT", "Mouse Right", "Mouse moves right")
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
        "Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Torque (Global)",
        "The local rotational velocity of the object"
    ), (
        "localAngularVelocity",
        "Torque (Local)",
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
    ("worldScale", "Scale", "The global scale of the object"),
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
        "Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Torque (Global)",
        "The local rotational velocity of the object"
    ), (
        "localAngularVelocity",
        "Torque (Local)",
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

_enum_math_operations = [
    ("ADD", "Add", "Sum A and B"),
    ("SUB", "Substract", "Subtract B from A"),
    ("DIV", "Divide", "Divide A by B"),
    ("MUL", "Multiply", "Multiply A by B")
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

OUTCELL = "__standard_logic_cell_value__"


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

    if t == "VECTOR":
        numbers = re.findall("[-+]?\d+[\.]?\d*", v)
        if len(numbers) == 2:
            return "mathutils.Vector(({},{}))".format(numbers[0], numbers[1])
        if len(numbers) == 3:
            return "mathutils.Vector(({},{},{}))".format(*numbers)
        if len(numbers) == 4:
            return "mathutils.Vector(({},{},{},{}))".format(*numbers)
        return "mathutils.Vector()"

    if t == "EULER":
        numbers = re.findall("[-+]?\d+[\.]?\d*", v)
        if len(numbers) == 1:
            return 'mathutils.Euler(({}, 0.0, 0.0), "XYZ")'.format(numbers[0])
        if len(numbers) == 2:
            return (
                'mathutils.Euler(({}, {}, 0.0), "XYZ")'.format(
                    numbers[0],
                    numbers[1]
                )
            )
        if len(numbers) == 3:
            return (
                'mathutils.Euler(({}, {}, {}), "XYZ")'.format(
                    numbers[0],
                    numbers[1],
                    numbers[2]
                )
            )
        return 'mathutils.Euler((0,0,0), "XYZ")'

    if t == "EXPRESSION":
        return v

    if t == "BOOLEAN":
        return v

    raise ValueError(
        "Cannot parse enum {} type for NLValueFieldSocket".format(t)
    )


def update_tree_code(self, context):
    bge_netlogic.update_current_tree_code()


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


class NetLogicSocketType:
    def get_unlinked_value(self):
        raise NotImplementedError()


class NetLogicStatementGenerator(NetLogicType):
    def write_cell_declaration(self, cell_varname, line_writer):
        classname = self.get_netlogic_class_name()
        line_writer.write_line("{} = {}()", cell_varname, classname)

    def init_cell_fields(
        self,
        cell_varname,
        uids,
        line_writer
    ):
        for t in self.get_nonsocket_fields():
            field_name = t[0]
            field_value = t[1]
            if callable(field_value):
                field_value = field_value()
            line_writer.write_line(
                '{}.{} = {}',
                cell_varname,
                field_name,
                field_value
            )
        for socket in self.inputs:
            self.write_socket_field_initialization(
                socket,
                cell_varname,
                uids,
                line_writer
            )

    def write_socket_field_initialization(
        self,
        socket,
        cell_varname,
        uids,
        line_writer
    ):
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
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            field_name,
            field_value
        )

    def get_nonsocket_fields(self):
        """
        Return a list of (field_name, field_value) tuples, where field_name
        couples to output socket with a cell field and field_value is
        either a value or a no-arg callable producing value
        :return: the non socket fields initializers
        """
        return []

    def get_input_sockets_field_names(self):
        return None

    def get_field_name_for_socket(self, socket):
        print("not implemented in ", self)
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
            next_socket = output_node.inputs[0].links[0].from_socket
            next_node = next_socket.node
            output_socket = next_socket
            if isinstance(next_node, NetLogicStatementGenerator):
                break
            output_node = next_node

        if isinstance(output_node, bpy.types.NodeReroute):
            output_node = output_node.inputs[0].links[0].from_socket.node
        output_socket_index = self._index_of(
            output_socket,
            output_node.outputs
        )

        if not isinstance(output_node, NetLogicStatementGenerator):
            print(output_node)
            print(output_node.__class__)
            raise Exception('No NetLogicStatementGenerator')
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
        bge_netlogic.update_current_tree_code()


class NLConditionSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLConditionSocket"
    bl_label = "Condition"
    default_value: bpy.props.StringProperty(
        name='Condition',
        default="None"
    )

    def draw_color(self, context, node):
        return CONDITION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self): return self.default_value


_sockets.append(NLConditionSocket)


class NLPseudoConditionSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPseudoConditionSocket"
    bl_label = "Condition"
    value: bpy.props.BoolProperty(
        name='Condition',
        description=(
            'Optional; When True, '
            'perform with each frame, when False, never perform'
        ),
        update=update_tree_code)

    def draw_color(self, context, node):
        return PSEUDO_COND_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            label = text
            layout.prop(self, "value", text=label)

    def get_unlinked_value(self):
        return "True" if self.value else "False"


_sockets.append(NLPseudoConditionSocket)


class NLParameterSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLParameterSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLParameterSocket)


class NLDictSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLDictSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAM_DICT_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLDictSocket)


class NLListSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLListSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAM_LIST_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLListSocket)


class NLLogicBrickSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLLogicBrickSocket"
    bl_label = "Logic Brick"

    def draw_color(self, context, node):
        return PARAM_LOGIC_BRICK_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLLogicBrickSocket)


class NLPythonSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPythonSocket"
    bl_label = "Python"

    def draw_color(self, context, node):
        return PARAM_PYTHON_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self):
        return "None"


_sockets.append(NLPythonSocket)


class NLActionSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLActionSocket"
    bl_label = "Action"

    def draw_color(self, context, node):
        return ACTION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)


_sockets.append(NLActionSocket)


class NLAbstractNode(NetLogicStatementGenerator):
    @classmethod
    def poll(cls, node_tree):
        pass

    def free(self):
        pass

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return self.__class__.bl_label


class NLConditionNode(NLAbstractNode):
    def init(self, context):
        self.use_custom_color = (
            bpy
            .context
            .scene
            .logic_node_settings
            .use_custom_node_color
        )
        self.color = CONDITION_NODE_COLOR


class NLActionNode(NLAbstractNode):
    def init(self, context):
        self.use_custom_color = (
            bpy
            .context
            .scene
            .logic_node_settings
            .use_custom_node_color
        )
        self.color = ACTION_NODE_COLOR


class NLParameterNode(NLAbstractNode):
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


class NLGameObjectSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLGameObjectSocket"
    bl_label = "Object"
    value: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )
    use_owner: bpy.props.BoolProperty(
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


_sockets.append(NLGameObjectSocket)


class NLMaterialSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLMaterialSocket"
    bl_label = "Material"
    value: bpy.props.PointerProperty(
        name='Material',
        type=bpy.types.Material,
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


class NLMeshSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLMeshSocket"
    bl_label = "Mesh"
    value: bpy.props.PointerProperty(
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


class NLGameObjectNameSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLGameObjectNameSocket"
    bl_label = "Object"
    value: bpy.props.PointerProperty(
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


class NLCollectionSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLCollectionSocket"
    bl_label = "Collection"
    value: bpy.props.PointerProperty(
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
            col.label(text=self.name)
            col.prop_search(
                self,
                'value',
                bpy.data,
                'collections',
                text=''
            )

    def get_unlinked_value(self):
        col_name = self.value.name
        if col_name.startswith('F '):
            col_name = col_name.split('F ')[-1]
        elif ' F ' in col_name:
            col_name = col_name.split(' F ')[-1]
        return "'{}'".format(col_name)


if not TOO_OLD:
    _sockets.append(NLCollectionSocket)


class NLSocketLogicTree(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketLogicTree"
    bl_label = "Logic Tree"
    value: bpy.props.PointerProperty(
        name='Logic Tree',
        type=bpy.types.NodeTree,
        description=(
            'Select a Logic Tree. '
            'NOTE: Selecting a Shader Node Group will result in an error!'
        ),
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        icon = 'OUTLINER' if not TOO_OLD else 'PLUS'
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop_search(
                self,
                "value",
                bpy.data,
                'node_groups',
                icon=icon,
                text=''
            )

    def get_unlinked_value(self):
        tree_name = self.value.name
        if tree_name.startswith('F '):
            tree_name = tree_name.split('F ')[-1]
        elif ' F ' in tree_name:
            tree_name = tree_name.split(' F ')[-1]
        return "'{}'".format(tree_name)


_sockets.append(NLSocketLogicTree)


class NLAnimationSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLAnimationSocket"
    bl_label = "Action"
    value: bpy.props.PointerProperty(
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
            if text:
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
        action_name = self.value.name
        if action_name.startswith('F '):
            action_name = action_name.split('F ')[-1]
        elif ' F ' in action_name:
            action_name = action_name.split(' F ')[-1]
        return "'{}'".format(action_name)


_sockets.append(NLAnimationSocket)


class NLSocketAlphaFloat(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketAlphaFloat"
    bl_label = "Factor"
    value: bpy.props.FloatProperty(
        name='Aplha Value',
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
            layout.prop(self, "value", text=text)
        pass

    def get_unlinked_value(self):
        return "{}".format(self.value)


_sockets.append(NLSocketAlphaFloat)


class NLSocketSound(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketSound"
    bl_label = "Sound"
    value: bpy.props.PointerProperty(
        name='Sound',
        type=bpy.types.Sound,
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return PARAM_SOUND_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=text)
        elif self.is_linked:
            layout.label(text=text)
        else:
            row = layout.row(align=True)
            row.prop_search(
                self,
                'value',
                bpy.context.blend_data,
                'sounds',
                icon='NONE',
                text=''
            )

    def get_unlinked_value(self):
        if self.value is None:
            return "{}".format(self.value)
        else:
            return "'{}'".format(self.value.filepath)


_sockets.append(NLSocketSound)


class NLSocketLogicOperator(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketLogicOperator"
    bl_label = "Logic Operator"
    value: bpy.props.EnumProperty(
        name='Logic Operators',
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


class NLSocketControllerButtons(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketControllerButtons"
    bl_label = "Controller Buttons"
    value: bpy.props.EnumProperty(
        name='Controller Buttons',
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


class NLSocketDistanceCheck(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketDistanceCheck"
    bl_label = "Distance Operator"
    value: bpy.props.EnumProperty(
        items=_enum_distance_checks,
        update=update_tree_code
    )
    def draw_color(self, context, node): return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self): return "{}".format(self.value)


_sockets.append(NLSocketDistanceCheck)


class NLSocketLoopCount(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketLoopCount"
    bl_label = "Loop Count"
    value: bpy.props.StringProperty(update=update_tree_code)

    def update_value(self, context):
        current_type = self.value_type
        if current_type == "INFINITE":
            self.value = "-1"
        elif current_type == "ONCE":
            self.value = "1"
        elif current_type == "CUSTOM":
            self.value = '{}'.format(int(self.integer_editor) - 1)
    value_type: bpy.props.EnumProperty(
        items=_enum_loop_count_values,
        update=update_value
    )
    integer_editor: bpy.props.IntProperty(
        update=update_value,
        min=1,
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


class NLBooleanSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLBooleanSocket"
    bl_label = "Boolean"
    value: bpy.props.BoolProperty(update=update_tree_code)
    use_toggle: bpy.props.BoolProperty(default=False)
    true_label: bpy.props.StringProperty()
    false_label: bpy.props.StringProperty()

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

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

    def get_unlinked_value(self): return "True" if self.value else "False"


_sockets.append(NLBooleanSocket)


class NLXYZSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLXYZSocket"
    bl_label = "Boolean"
    x: bpy.props.BoolProperty(update=update_tree_code, default=True)
    y: bpy.props.BoolProperty(update=update_tree_code, default=True)
    z: bpy.props.BoolProperty(update=update_tree_code, default=True)

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
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }


_sockets.append(NLXYZSocket)


class NLInvertedXYSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLInvertedXYSocket"
    bl_label = "Boolean"
    x: bpy.props.BoolProperty(update=update_tree_code)
    y: bpy.props.BoolProperty(update=update_tree_code)

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
        return {
            'x': self.x,
            'y': self.y
        }


_sockets.append(NLInvertedXYSocket)


class NLPositiveFloatSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPositiveFloatSocket"
    bl_label = "Positive Float"
    value: bpy.props.FloatProperty(min=0.0, update=update_tree_code)

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


class NLPosFloatFormatSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPosFloatFormatSocket"
    bl_label = "Positive Float"
    value: bpy.props.FloatProperty(min=0.0, update=update_tree_code)

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


class NLSocketOptionalPositiveFloat(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketOptionalPositiveFloat"
    bl_label = "Positive Float"
    use_this: bpy.props.BoolProperty(update=update_tree_code)
    value: bpy.props.StringProperty(update=update_tree_code)

    def update_value(self, context):
        if self.use_this:
            self.value = '{}'.format(self.float_editor)
        else:
            self.value = ""

        update_tree_code(self, context)

    float_editor: bpy.props.FloatProperty(
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


class NLSocketIKMode(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketIKMode"
    bl_label = "IK Mode"
    value: bpy.props.EnumProperty(
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
        return self.value


_sockets.append(NLSocketIKMode)


class NLAlphaSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLAlphaSocket"
    bl_label = "Alpha Float"
    value: bpy.props.StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self):
        if not self.value:
            return None
        try:
            return float(self.value)
        except ValueError:
            return None


_sockets.append(NLAlphaSocket)


class NLQuotedStringFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLQuotedStringFieldSocket"
    bl_label = "String"
    value: bpy.props.StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        elif not text:
            layout.prop(self, "value", text='')
        else:
            parts = layout.split()
            parts.label(text=text)
            parts.prop(self, "value", text='')

    def get_unlinked_value(self): return '"{}"'.format(self.value)
    pass


_sockets.append(NLQuotedStringFieldSocket)


class NLFilePathSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLFilePathSocket"
    bl_label = "String"
    value: bpy.props.StringProperty(
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


class NLIntegerFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLIntegerFieldSocket"
    bl_label = "Integer"
    value: bpy.props.IntProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return '{}'.format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
    pass


_sockets.append(NLIntegerFieldSocket)


class NLPositiveIntegerFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPositiveIntegerFieldSocket"
    bl_label = "Integer"
    value: bpy.props.IntProperty(min=0, default=0, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    def get_unlinked_value(self): return '{}'.format(self.value)
    pass


_sockets.append(NLPositiveIntegerFieldSocket)


class NLSceneSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSceneSocket"
    bl_label = "Scene"

    def draw_color(self, context, node):
        return PARAM_SCENE_SOCKET_COLOR

    def get_unlinked_value(self): return "None"

    def draw(self, context, layout, node, text):
        layout.label(text=text)


_sockets.append(NLSceneSocket)


class NLValueFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLValueFieldSocket"
    bl_label = "Value"
    value: bpy.props.StringProperty(update=update_tree_code)

    def on_type_changed(self, context):
        if self.value_type == "BOOLEAN":
            self.value = str(self.bool_editor)
        update_tree_code(self, context)

    value_type: bpy.props.EnumProperty(
        items=_enum_field_value_types,
        update=on_type_changed
    )

    def store_boolean_value(self, context):
        self.value = str(self.bool_editor)
        update_tree_code(self, context)

    bool_editor: bpy.props.BoolProperty(update=store_boolean_value)

    def store_int_value(self, context):
        self.value = str(self.int_editor)

    int_editor: bpy.props.IntProperty(update=store_int_value)

    def store_float_value(self, context):
        self.value = str(self.float_editor)

    float_editor: bpy.props.FloatProperty(update=store_float_value)

    def store_string_value(self, context):
        self.value = self.string_editor

    string_editor: bpy.props.StringProperty(update=store_string_value)

    def store_path_value(self, context):
        self.value = self.path_editor

    path_editor: bpy.props.StringProperty(
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


class NLNumericFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLNumericFieldSocket"
    bl_label = "Value"

    value_type: bpy.props.EnumProperty(
        items=_enum_numeric_field_value_types,
        update=update_tree_code
    )
    value: bpy.props.StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self): return socket_field(self)

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


class NLOptionalRadiansFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLOptionalRadiansFieldSocket"
    bl_label = "Value"
    value: bpy.props.StringProperty(update=update_tree_code, default="0.0")

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
    float_field: bpy.props.FloatProperty(update=store_radians)
    expression_field: bpy.props.StringProperty(update=store_expression)
    input_type: bpy.props.EnumProperty(
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


class NLSocketReadableMemberName(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketReadableMemberName"
    bl_label = "Att. Name"
    value: bpy.props.StringProperty(
        update=update_tree_code,
        default='worldPosition'
    )

    def _set_value(self, context):
        t = self.value_type
        if t == "CUSTOM":
            self.value = ""
        else:
            self.value = t
        bge_netlogic.update_current_tree_code()
    value_type: bpy.props.EnumProperty(
        items=_enum_readable_member_names,
        update=_set_value
    )

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR if (
            self.value != 'name' and
            self.value != 'visible'
        ) else PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self): return '"{}"'.format(self.value)

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


class NLKeyboardKeySocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLKeyboardKeySocket"
    bl_label = "Key"
    value: bpy.props.StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

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


class NLSocketKeyboardKeyPressed(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketKeyboardKeyPressed"
    bl_label = "Key"
    value: bpy.props.StringProperty(update=update_tree_code)

    def draw_color(self, context, node):
        return CONDITION_SOCKET_COLOR

    def get_unlinked_value(self):
        bge_key = keyboard_key_string_to_bge_key(self.value)
        return 'network.add_cell(\
            bgelogic.ConditionKeyPressed(\
                pulse=True, key_code={}))\
                    '.format(bge_key)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)
            label = self.value
            if not label:
                label = "Press & Choose"
            layout.operator("bge_netlogic.waitforkey", text=label)


_sockets.append(NLSocketKeyboardKeyPressed)


class NLMouseButtonSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLMouseButtonSocket"
    bl_label = "Mouse Button"
    value: bpy.props.EnumProperty(
        items=_enum_mouse_buttons, default="bge.events.LEFTMOUSE",
        update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self): return self.value

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text="")


_sockets.append(NLMouseButtonSocket)


class NLVSyncSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVSyncSocket"
    bl_label = "Vsync"
    value: bpy.props.EnumProperty(
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


class NLPlayActionModeSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLPlayActionModeSocket"
    bl_label = "Play Mode"
    value: bpy.props.EnumProperty(
        items=_enum_play_mode_values,
        description="The play mode of the action",
        update=update_tree_code
    )

    def get_unlinked_value(self): return self.value

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLPlayActionModeSocket)


class NLFloatFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLFloatFieldSocket"
    bl_label = "Float Value"
    value: bpy.props.FloatProperty(default=0, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self): return "{}".format(self.value)

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)


_sockets.append(NLFloatFieldSocket)


class NLVec2FieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVec2FieldSocket"
    bl_label = "Float Value"
    value_x: bpy.props.FloatProperty(default=0, update=update_tree_code)
    value_y: bpy.props.FloatProperty(default=0, update=update_tree_code)
    title: bpy.props.StringProperty(default='')

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


class NLVec2PositiveFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVec2PositiveFieldSocket"
    bl_label = "Float Value"
    value_x: bpy.props.FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    value_y: bpy.props.FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    title: bpy.props.StringProperty(default='')

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


class NLVec3FieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVec3FieldSocket"
    bl_label = "Float Value"
    value_x: bpy.props.FloatProperty(default=0, update=update_tree_code)
    value_y: bpy.props.FloatProperty(default=0, update=update_tree_code)
    value_z: bpy.props.FloatProperty(default=0, update=update_tree_code)

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}))".format(
            self.value_x,
            self.value_y,
            self.value_z
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column(align=True)
            if text != '':
                column.label(text=text)
            column.prop(self, "value_x", text='X')
            column.prop(self, "value_y", text='Y')
            column.prop(self, "value_z", text='Z')


_sockets.append(NLVec3FieldSocket)


class NLVec3PositiveFieldSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVec3PositiveFieldSocket"
    bl_label = "Float Value"
    value_x: bpy.props.FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    value_y: bpy.props.FloatProperty(
        min=0.0,
        default=0,
        update=update_tree_code
    )
    value_z: bpy.props.FloatProperty(default=0, update=update_tree_code)
    title: bpy.props.StringProperty(default='')

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def get_unlinked_value(self):
        return "mathutils.Vector(({}, {}, {}))".format(
            self.value_x,
            self.value_y,
            self.value_z
        )

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            column = layout.column()
            # if self.title != '':
            #     title = column.label(text=self.title)
            column.prop(self, "value_x", text='X')
            column.prop(self, "value_y", text='Y')
            column.prop(self, "value_z", text='Z')


_sockets.append(NLVec3PositiveFieldSocket)


class NLBlendActionModeSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLBlendActionMode"
    bl_label = "Blend Mode"
    value: bpy.props.EnumProperty(
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


class NLSocketMouseMotion(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketMouseMotion"
    bl_label = "Mouse Motion"
    value: bpy.props.EnumProperty(
        items=_enum_mouse_motion,
        description="The direction of the mouse movement",
        update=update_tree_code
    )

    def draw_color(self, context, node):
        return CONDITION_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)
            layout.prop(self, "value", text="")

    def get_unlinked_value(self):
        if self.value == "UP":
            return "network.add_cell(bgelogic.ConditionMouseUp(repeat=True))"

        if self.value == "DOWN":
            return "network.add_cell(bgelogic.ConditionMouseDown(repeat=True))"

        if self.value == "LEFT":
            return "network.add_cell(bgelogic.ConditionMouseLeft(repeat=True))"

        if self.value == "RIGHT":
            return (
                "network.add_cell(bgelogic.ConditionMouseRight(repeat=True))"
            )


_sockets.append(NLSocketMouseMotion)


class NLVectorSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVectorSocket"
    bl_label = "Parameter"

    def draw_color(self, context, node):
        return PARAM_VECTOR_SOCKET_COLOR

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_unlinked_value(self): return "None"


_sockets.append(NLVectorSocket)


class NLSocketVectorField(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketVectorField"
    bl_label = "Vector"
    value: bpy.props.StringProperty(
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


class NLOptionalSocketVectorField(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLOptionalSocketVectorField"
    bl_label = "Vector"
    value: bpy.props.StringProperty(
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


class NLSocketOptionalFilePath(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketOptionalFilePath"
    bl_label = "File"
    value: bpy.props.StringProperty(
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


class NLSocketMouseWheelDirection(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketMouseWheelDirection"
    bl_label = "Mouse Wheel"
    value: bpy.props.EnumProperty(
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


class NLSocketDistanceModels(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketDistanceModels"
    bl_label = "Distance Model"
    value: bpy.props.EnumProperty(
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


class NLVectorMathSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLVectorMathSocket"
    bl_label = "Vector Math"
    value: bpy.props.EnumProperty(
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


class NLTypeCastSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLTypeCastSocket"
    bl_label = "Types"
    value: bpy.props.EnumProperty(
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


class NLConstraintTypeSocket(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLConstraintTypeSocket"
    bl_label = "Constraint Type"
    value: bpy.props.EnumProperty(
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


class NLSocketFilter3(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketFilter3"
    bl_label = "Filter 3"
    value: bpy.props.EnumProperty(
        items=_enum_value_filters_3,
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


_sockets.append(NLSocketFilter3)


class NLSocketLocalAxis(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketLocalAxis"
    bl_label = "Local Axis"
    value: bpy.props.EnumProperty(
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

    def get_unlinked_value(self): return self.value


_sockets.append(NLSocketLocalAxis)


class NLSocketOrientedLocalAxis(bpy.types.NodeSocket, NetLogicSocketType):
    bl_idname = "NLSocketOrientedLocalAxis"
    bl_label = "Local Axis"
    value: bpy.props.EnumProperty(
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


class NLParameterConstantValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterConstantValue"
    bl_label = "Value"
    nl_category = "Values"

    def on_type_changed(self, context):
        tp = self.value_type
        if tp == "BOOLEAN":
            self.value = "True" if (self.bool_editor == "True") else "False"
        update_tree_code(self, context)
        pass
    value_type: bpy.props.EnumProperty(
        items=_enum_field_value_types,
        update=on_type_changed
    )

    value: bpy.props.StringProperty(update=update_tree_code)

    def store_boolean_value(self, context):
        self.value = "True" if (self.bool_editor == "True") else "False"
        update_tree_code(self, context)
    bool_editor: bpy.props.EnumProperty(
        items=_enum_boolean_values,
        update=store_boolean_value
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def draw_buttons(self, context, layout):
        split = layout
        if self.value_type == "NONE":
            split.prop(self, "value_type", text="")
        elif self.value_type == "BOOLEAN":
            row = split.row(align=True)
            row.prop(self, "value_type", text="")
            row.prop(self, "bool_editor", text="")
        else:
            row = split.row(align=True)
            row.prop(self, "value_type", text="")
            row.prop(self, "value", text="")

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "")

    def get_nonsocket_fields(self):
        v = parse_field_value(self.value_type, self.value)
        return [("value", v)]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterConstantValue"


# _nodes.append(NLParameterConstantValue)


class NLParameterFindChildByNameNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterFindChildByNameNode"
    bl_label = "Get Child By Name"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Parent")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "Child")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Child")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterFindChildByName"

    def get_input_sockets_field_names(self):
        return ["from_parent", "child"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLParameterFindChildByNameNode)


class NLParameterSound(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterSound"
    bl_label = "Sound"
    nl_category = "Sound"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLSocketOptionalFilePath.bl_idname, "File")
        self.outputs.new(NLSocketSound.bl_idname, "Sound")
        self.outputs.new(NLConditionSocket.bl_idname, "Is Playing")
        self.outputs.new(NLParameterSocket.bl_idname, "Current Frame")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterSound"

    def get_input_sockets_field_names(self):
        return ["file_path"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "IS_PLAYING", "CURRENT_FRAME"]


# _nodes.append(NLParameterSound)


class NLParameterValueFilter3(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterValueFilter"
    bl_label = "Limit Range"
    nl_category = "Math"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLSocketFilter3.bl_idname, "Op")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Lower Limit")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Upper Limit")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterValueFilter3"

    def get_input_sockets_field_names(self):
        return ["opcode", "parama", "paramb", "paramc"]


# _nodes.append(NLParameterValueFilter3)


class NLParameterGetAttribute(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterGetAttribute"
    bl_label = "Get Object Attribute"
    nl_category = "Python"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPythonSocket.bl_idname, "Object Instance")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.GetObInstanceAttr"

    def get_input_sockets_field_names(self):
        return ['instance', 'attr']


_nodes.append(NLParameterGetAttribute)


class NLParameterGetTimeScale(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterGetTimeScale"
    bl_label = "Get Timescale"
    nl_category = "Scene"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Timescale")

    def get_netlogic_class_name(self):
        return "bgelogic.GetTimeScale"


_nodes.append(NLParameterGetTimeScale)


class NLParameterScreenPosition(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterScreenPosition"
    bl_label = "Screen Position"
    nl_category = "Scene"
    nl_subcat = 'Camera'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object / Vector 3")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Camera")
        self.outputs.new(NLParameterSocket.bl_idname, "Screen X")
        self.outputs.new(NLParameterSocket.bl_idname, "Screen Y")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterScreenPosition"

    def get_input_sockets_field_names(self):
        return ["game_object", "camera"]

    def get_output_socket_varnames(self):
        return ["xposition", "yposition"]


_nodes.append(NLParameterScreenPosition)


class NLParameterWorldPosition(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterWorldPosition"
    bl_label = "World Position"
    nl_category = "Scene"
    nl_subcat = 'Camera'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Camera")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen X")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Screen Y")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Depth")
        self.outputs.new(NLParameterSocket.bl_idname, "World Position")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterWorldPosition"

    def get_input_sockets_field_names(self):
        return ["camera", "screen_x", "screen_y", "world_z"]


_nodes.append(NLParameterWorldPosition)


class NLOwnerGameObjectParameterNode(bpy.types.Node, NLParameterNode):
    """The owner of this logic tree.
    Each Object that has this tree installed is
    the "owner" of a logic tree
    """
    bl_idname = "NLOwnerGameObjectParameterNode"
    bl_label = "Get Owner"
    bl_icon = 'USER'
    nl_category = "Objects"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLGameObjectSocket.bl_idname, "Owner Object")

    def get_netlogic_class_name(self):
        return "bgelogic.ParamOwnerObject"


_nodes.append(NLOwnerGameObjectParameterNode)


class NLGetVsyncNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetVsyncNode"
    bl_label = "Get VSync"
    nl_category = 'Render'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Mode")

    def get_netlogic_class_name(self):
        return "bgelogic.GetVSync"


_nodes.append(NLGetVsyncNode)


class NLGetFullscreen(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetFullscreen"
    bl_label = "Get Fullscreen"
    nl_category = 'Render'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Fullscreen")

    def get_netlogic_class_name(self):
        return "bgelogic.GetFullscreen"


_nodes.append(NLGetFullscreen)


class NLGetResolution(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetResolution"
    bl_label = "Get Resolution"
    nl_category = 'Render'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLParameterSocket.bl_idname, "Width")
        self.outputs.new(NLParameterSocket.bl_idname, "Height")
        self.outputs.new(NLVec2FieldSocket.bl_idname, "Resolution")

    def get_netlogic_class_name(self):
        return "bgelogic.GetResolution"

    def get_output_socket_varnames(self):
        return ['WIDTH', 'HEIGHT', 'RES']


_nodes.append(NLGetResolution)


class NLGameObjectPropertyParameterNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGameObjectPropertyParameterNode"
    bl_label = "Get Property"
    bl_icon = 'EXPORT'
    nl_category = 'Objects'
    nl_subcat = 'Properties'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.outputs.new(NLParameterSocket.bl_idname, "Property Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterObjectProperty"

    def get_input_sockets_field_names(self):
        return ["game_object", "property_name"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGameObjectPropertyParameterNode)


class NLGetMaterialNodeValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLGetMaterialNodeValue"
    bl_label = "Get Node Input Value"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Node Name")
        self.inputs[-1].value = 'Node'
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterGetMaterialNodeValue"

    def get_input_sockets_field_names(self):
        return ["mat_name", 'node_name', "input_slot"]

    def get_output_socket_varnames(self):
        return ['OUT']


if not TOO_OLD:
    _nodes.append(NLGetMaterialNodeValue)


class NLGetMaterialNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLGetMaterialNode"
    bl_label = "Get Node"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Node Name")
        self.inputs[-1].value = 'Node'
        self.outputs.new(NLParameterSocket.bl_idname, "Node")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterGetMaterialNode"

    def get_input_sockets_field_names(self):
        return ["mat_name", 'node_name']

    def get_output_socket_varnames(self):
        return ['OUT']


if not TOO_OLD:
    _nodes.append(NLGetMaterialNode)


class NLGetMaterialNodeInput(bpy.types.Node, NLActionNode):
    bl_idname = "NLGetMaterialNodeInput"
    bl_label = "Get Input"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Material Node")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Input")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterGetMaterialNodeIndex"

    def get_input_sockets_field_names(self):
        return ["node", 'input_slot']

    def get_output_socket_varnames(self):
        return ['OUT']


if not TOO_OLD:
    _nodes.append(NLGetMaterialNodeInput)


class NLGetMaterialNodeInputValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLGetMaterialNodeInputValue"
    bl_label = "Get Input Value"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Input")
        self.outputs.new(NLParameterSocket.bl_idname, "Input")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterGetMaterialInputValue"

    def get_input_sockets_field_names(self):
        return ['input']

    def get_output_socket_varnames(self):
        return ['OUT']


if not TOO_OLD:
    _nodes.append(NLGetMaterialNodeInputValue)


class NLGameObjectHasPropertyParameterNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGameObjectHasPropertyParameterNode"
    bl_label = "Has Property"
    bl_icon = 'QUESTION'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterObjectHasProperty"

    def get_input_sockets_field_names(self):
        return ["game_object", "property_name"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGameObjectHasPropertyParameterNode)


class NLGetDictKeyNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetDictKeyNode"
    bl_label = 'Get Key'
    nl_category = "Python"
    nl_subcat = 'Dictionary'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLDictSocket.bl_idname, "Dictionary")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Key")
        self.inputs[-1].value = 'key'
        self.outputs.new(NLParameterSocket.bl_idname, "Property Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterDictionaryValue"

    def get_input_sockets_field_names(self):
        return ["dict", "key"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetDictKeyNode)


class NLGetRandomListIndex(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetRandomListIndex"
    bl_label = "Get Random Item"
    nl_category = "Python"
    nl_subcat = 'List'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLListSocket.bl_idname, "List")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterRandomListIndex"

    def get_input_sockets_field_names(self):
        return ["condition", "list"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetRandomListIndex)


class NLGetListIndexNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetListIndexNode"
    bl_label = "Get Index"
    nl_category = "Python"
    nl_subcat = 'List'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLListSocket.bl_idname, "List")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Index")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterListIndex"

    def get_input_sockets_field_names(self):
        return ["list", "index"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetListIndexNode)


class NLGetActuatorNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetActuatorNode"
    bl_label = "Get Actuator"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    obj: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )
    actuator: bpy.props.StringProperty(update=update_tree_code)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLLogicBrickSocket.bl_idname, "Actuator")

    def get_netlogic_class_name(self): return "bgelogic.GetActuator"

    def draw_buttons(self, context, layout):
        col = layout.column()
        row1 = col.row()
        row2 = col.row()
        row1.label(text='From Object')
        row2.prop_search(
            self,
            "obj",
            bpy.context.scene,
            'objects',
            icon='NONE',
            text=''
        )
        if self.obj:
            row3 = col.row()
            row4 = col.row()
            row3.label(text='Actuator')
            row4.prop_search(
                self,
                "actuator",
                self.obj.game,
                'actuators',
                icon='NONE',
                text=''
            )

    def get_nonsocket_fields(self):
        return [
            (
                "obj_name", lambda: 'bgelogic.GetActuator.obj("{}")'.format(
                    'Object:{}'.format(self.obj.name)
                )
            ),
            (
                "act_name", lambda: 'bgelogic.GetActuator.act("{}")'.format(
                    self.actuator
                )
            )
        ] if self.obj else []

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetActuatorNode)


class NLGetActuatorNameNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetActuatorNameNode"
    bl_label = "Get Actuator By Name"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Actuator Name")
        self.outputs.new(NLLogicBrickSocket.bl_idname, "Actuator")

    def get_netlogic_class_name(self):
        return "bgelogic.GetActuatorByName"

    def get_input_sockets_field_names(self):
        return ["act_name"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetActuatorNameNode)


class NLGetActuatorValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetActuatorValue"
    bl_label = "Get Actuator Value"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator Name")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Field")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.GetActuatorValue"

    def get_input_sockets_field_names(self):
        return ["actuator", 'field']

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetActuatorValue)


class NLRunActuatorNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLRunActuatorNode"
    bl_label = "Execute Actuator"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self): return "bgelogic.ActivateActuator"

    def get_input_sockets_field_names(self):
        return ["condition", 'actuator']


_nodes.append(NLRunActuatorNode)


class NLDisableActuatorNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLDisableActuatorNode"
    bl_label = "Stop Actuator"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self): return "bgelogic.DeactivateActuator"

    def get_input_sockets_field_names(self):
        return ["condition", 'actuator']


_nodes.append(NLDisableActuatorNode)


class NLRunActuatorByNameNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLRunActuatorByNameNode"
    bl_label = "Execute Actuator By Name"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Actuator")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self): return "bgelogic.ActivateActuatorByName"

    def get_input_sockets_field_names(self):
        return ["condition", 'actuator']


_nodes.append(NLRunActuatorByNameNode)


class NLDisableActuatorByNameNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLDisableActuatorByNameNode"
    bl_label = "Stop Actuator By Name"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Actuator")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.DeactivateActuatorByName"

    def get_input_sockets_field_names(self):
        return ["condition", 'actuator']


_nodes.append(NLDisableActuatorByNameNode)


class NLSetActuatorValueNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetActuatorValueNode"
    bl_label = "Set Actuator Value"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLLogicBrickSocket.bl_idname, "Actuator")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Field")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self): return "bgelogic.SetActuatorValue"

    def get_input_sockets_field_names(self):
        return ["condition", 'actuator', 'field', 'value']


_nodes.append(NLSetActuatorValueNode)


class NLVectorMath(bpy.types.Node, NLParameterNode):
    bl_idname = "NLVectorMath"
    bl_label = "Vector Math"
    nl_category = "Math"
    nl_subcat = 'Vector Math'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVectorMathSocket.bl_idname, '')
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 1")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector 2")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.outputs.new(NLParameterSocket.bl_idname, 'Vector')

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterVectorMath"

    def get_input_sockets_field_names(self):
        return ['op', "vector", 'vector_2', 'factor']


_nodes.append(NLVectorMath)


class NLGetSensorNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetSensorNode"
    bl_label = "Sensor Positive"
    nl_category = "Logic"
    nl_subcat = 'Bricks'
    obj: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )
    sensor: bpy.props.StringProperty(update=update_tree_code)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "If positive")

    def get_netlogic_class_name(self):
        return "bgelogic.GetSensor"

    def draw_buttons(self, context, layout):
        col = layout.column()
        row1 = col.row()
        row2 = col.row()
        row1.label(text='From Object')
        row2.prop_search(
            self,
            "obj",
            bpy.context.scene,
            'objects',
            icon='NONE',
            text=''
        )
        if self.obj:
            row3 = col.row()
            row4 = col.row()
            row3.label(text='Sensor')
            row4.prop_search(
                self,
                "sensor",
                self.obj.game,
                'sensors',
                icon='NONE',
                text=''
            )

    def get_nonsocket_fields(self):
        return [
            (
                "obj_name", lambda: 'bgelogic.GetSensor.obj("{}")'.format(
                    'Object:{}'.format(self.obj.name)
                )
            ),
            (
                "sens_name", lambda: 'bgelogic.GetSensor.sens("{}")'.format(
                    self.sensor
                )
            )
        ] if self.obj else []

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetSensorNode)


class NLGetSensorNameNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetSensorNameNode"
    bl_label = "Sensor Positive by Name"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "From Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Sensor Name")
        self.outputs.new(NLConditionSocket.bl_idname, "If positive")

    def get_input_sockets_field_names(self):
        return ["obj", "name"]

    def get_netlogic_class_name(self):
        return "bgelogic.GetSensorByName"

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetSensorNameNode)


class NLGetSensorValueNameNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetSensorValueNameNode"
    bl_label = "Get Sensor Value by Name"
    nl_category = "Logic"
    nl_subcat = 'Bricks'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "From Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Sensor Name")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Field")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["obj", "name", 'field']

    def get_netlogic_class_name(self):
        return "bgelogic.GetSensorValueByName"

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLGetSensorValueNameNode)


class NLSensorValueNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLSensorValueNode"
    bl_label = "Get Sensor Value"
    nl_category = 'Logic'
    nl_subcat = 'Bricks'
    obj: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object,
        update=update_tree_code
    )
    sensor: bpy.props.StringProperty(update=update_tree_code)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Field')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self): return "bgelogic.SensorValue"

    def get_input_sockets_field_names(self):
        return ["field"]

    def draw_buttons(self, context, layout):
        col = layout.column()
        row1 = col.row()
        row2 = col.row()
        row1.label(text='From Object')
        row2.prop_search(
            self,
            "obj",
            bpy.context.scene,
            'objects',
            icon='NONE',
            text=''
        )
        if self.obj:
            row3 = col.row()
            row4 = col.row()
            row3.label(text='Sensor')
            row4.prop_search(
                self,
                "sensor",
                self.obj.game,
                'sensors',
                icon='NONE',
                text=''
            )

    def get_nonsocket_fields(self):
        return [
            (
                "obj_name", lambda: 'bgelogic.SensorValue.obj("{}")'.format(
                    'Object:{}'.format(self.obj.name)
                )
            ),
            (
                "sens_name", lambda: 'bgelogic.SensorValue.sens("{}")'.format(
                    self.sensor
                )
            )
        ] if self.obj else []

    def get_output_socket_varnames(self):
        return ['OUT', 'VAL']


_nodes.append(NLSensorValueNode)


class NLObjectAttributeParameterNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLObjectAttributeParameterNode"
    bl_label = "Get Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Data'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLSocketReadableMemberName.bl_idname, "Value")
        self.inputs[-1].value = 'worldPosition'
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterObjectAttribute"

    def get_input_sockets_field_names(self):
        return ["game_object", "attribute_name"]


_nodes.append(NLObjectAttributeParameterNode)


class NLActiveCameraParameterNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLActiveCameraParameterNode"
    bl_label = "Active Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLGameObjectSocket.bl_idname, "Camera")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterActiveCamera"


_nodes.append(NLActiveCameraParameterNode)


class NLGetCollectionNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    bl_icon = 'OUTLINER_COLLECTION'
    nl_category = "Scene"
    nl_subcat = 'Collections'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, '')
        self.outputs.new(NLCollectionSocket.bl_idname, "Collection")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "bgelogic.GetCollection"


_nodes.append(NLGetCollectionNode)


class NLGetCollectionObjectsNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetCollectionObjectsNode"
    bl_label = "Get Objects"
    nl_category = "Scene"
    nl_subcat = 'Collections'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLListSocket.bl_idname, "Objects")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "bgelogic.GetCollectionObjects"


_nodes.append(NLGetCollectionObjectsNode)


class NLGetCollectionObjectNamesNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetCollectionObjectNamesNode"
    bl_label = "Get Object Names"
    nl_category = "Scene"
    nl_subcat = 'Collections'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLCollectionSocket.bl_idname, 'Collection')
        self.outputs.new(NLListSocket.bl_idname, "Objects")

    def get_input_sockets_field_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "bgelogic.GetCollectionObjectNames"


_nodes.append(NLGetCollectionObjectNamesNode)


class NLArithmeticOpParameterNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLArithmeticOpParameterNode"
    bl_label = "Math"
    nl_category = "Math"
    operator: bpy.props.EnumProperty(
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

    def get_nonsocket_fields(self):
        return [
                (
                    "operator", lambda:
                    'bgelogic.ParameterArithmeticOp.op_by_code("{}")'.format(
                        self.operator
                    )
                )
            ]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterArithmeticOp"

    def get_input_sockets_field_names(self):
        return ["operand_a", "operand_b"]


_nodes.append(NLArithmeticOpParameterNode)


class NLThresholdNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLThresholdNode"
    bl_label = "Threshold"
    nl_category = "Math"
    operator: bpy.props.EnumProperty(
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

    def get_nonsocket_fields(self):
        return [
                (
                    "operator", lambda:
                    'bgelogic.Threshold.op_by_code("{}")'.format(
                        self.operator
                    )
                )
            ]

    def get_netlogic_class_name(self):
        return "bgelogic.Threshold"

    def get_input_sockets_field_names(self):
        return ['else_z', "value", "threshold"]


_nodes.append(NLThresholdNode)


class NLRangedThresholdNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLRangedThresholdNode"
    bl_label = "Ranged Threshold"
    nl_category = "Math"
    operator: bpy.props.EnumProperty(
        items=_enum_greater_less,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Threshold")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_nonsocket_fields(self):
        return [
                (
                    "operator", lambda:
                    'bgelogic.RangedThreshold.op_by_code("{}")'.format(
                        self.operator
                    )
                )
            ]

    def get_netlogic_class_name(self):
        return "bgelogic.RangedThreshold"

    def get_input_sockets_field_names(self):
        return ["value", "threshold"]


_nodes.append(NLRangedThresholdNode)


class NLWithinRangeNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLWithinRangeNode"
    bl_label = "Within Range"
    nl_category = "Math"
    operator: bpy.props.EnumProperty(
        items=_enum_in_or_out,
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Range")
        self.outputs.new(NLParameterSocket.bl_idname, "If True")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_nonsocket_fields(self):
        return [
                (
                    "operator", lambda:
                    'bgelogic.WithinRange.op_by_code("{}")'.format(
                        self.operator
                    )
                )
            ]

    def get_netlogic_class_name(self):
        return "bgelogic.WithinRange"

    def get_input_sockets_field_names(self):
        return ["value", "range"]


_nodes.append(NLWithinRangeNode)


class NLClampValueNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLClampValueNode"
    bl_label = "Clamp"
    nl_category = "Math"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ClampValue"

    def get_input_sockets_field_names(self):
        return ["value", "range"]


_nodes.append(NLClampValueNode)


class NLInterpolateValueNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLInterpolateValueNode"
    bl_label = "Interpolate"
    nl_category = "Math"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "From")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "To")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.InterpolateValue"

    def get_input_sockets_field_names(self):
        return ["value_a", "value_b", "factor", "range"]


_nodes.append(NLInterpolateValueNode)


class NLParameterActionStatus(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterActionStatus"
    bl_label = "Animation Status"
    nl_category = "Animation"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.outputs.new(NLConditionSocket.bl_idname, "Is Playing")
        self.outputs.new(NLConditionSocket.bl_idname, "Not Playing")
        self.outputs.new(NLParameterSocket.bl_idname, "Action Name")
        self.outputs.new(NLParameterSocket.bl_idname, "Action Frame")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterActionStatus"

    def get_input_sockets_field_names(self):
        return ["game_object", "action_layer"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "NOT_PLAYING", "ACTION_NAME", "ACTION_FRAME"]


_nodes.append(NLParameterActionStatus)


class NLParameterSwitchValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterSwitchValue"
    bl_label = "True / False"
    nl_category = "Logic"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLPseudoConditionSocket.bl_idname, "True")
        self.outputs.new(NLPseudoConditionSocket.bl_idname, "False")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterSwitchValue"

    def get_input_sockets_field_names(self):
        return ["state"]

    def get_output_socket_varnames(self):
        return ["TRUE", "FALSE"]


_nodes.append(NLParameterSwitchValue)


class NLParameterTimeNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterTimeNode"
    bl_label = "Time Data"
    nl_category = 'Time'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Frames Per Second")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Time Per Frame")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Total Elapsed Time")

    def get_output_socket_varnames(self):
        return ["FPS", "TIME_PER_FRAME", "TIMELINE"]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterTime"


_nodes.append(NLParameterTimeNode)


class NLMouseDataParameter(bpy.types.Node, NLParameterNode):
    bl_idname = "NLMouseDataParameter"
    bl_label = "Status"
    bl_icon = 'OPTIONS'
    nl_category = "Input"
    nl_subcat = 'Mouse'

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
        return "bgelogic.ParameterMouseData"

    def get_output_socket_varnames(self):
        return ["MXY0", "MDXY0", "MX", "MY", "MDX", "MDY", "MDWHEEL"]


_nodes.append(NLMouseDataParameter)


class NLParameterOrientationNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterOrientationNode"
    bl_label = "Orientation"
    nl_category = "Math"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLOptionalRadiansFieldSocket.bl_idname, "X Rad")
        self.inputs.new(NLOptionalRadiansFieldSocket.bl_idname, "Y Rad")
        self.inputs.new(NLOptionalRadiansFieldSocket.bl_idname, "Z Rad")
        self.inputs.new(NLParameterSocket.bl_idname, "Orientation")
        self.outputs.new(NLParameterSocket.bl_idname, "Orientation")
        self.outputs.new(NLParameterSocket.bl_idname, "Rad Euler")
        self.outputs.new(NLParameterSocket.bl_idname, "X")
        self.outputs.new(NLParameterSocket.bl_idname, "Y")
        self.outputs.new(NLParameterSocket.bl_idname, "Z")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterOrientation"

    def get_output_socket_varnames(self):
        return [OUTCELL, "OUTEULER", "OUTX", "OUTY", "OUTZ"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z", "source_matrix"]


_nodes.append(NLParameterOrientationNode)


class NLParameterBoneStatus(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterBoneStatus"
    bl_label = "Armature Bone Status"
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Armature Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Bone Name")
        self.outputs.new(NLParameterSocket.bl_idname, "Position")
        self.outputs.new(NLParameterSocket.bl_idname, "Rotation")
        self.outputs.new(NLParameterSocket.bl_idname, "Scale")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterBoneStatus"

    def get_input_sockets_field_names(self):
        return ["armature", "bone_name"]

    def get_output_socket_varnames(self):
        return ["XYZ_POS", "XYZ_ROT", "XYZ_SCA"]


_nodes.append(NLParameterBoneStatus)


class NLParameterPythonModuleFunction(bpy.types.Node, NLActionNode):
    bl_idname = "NLParameterPythonModuleFunction"
    bl_label = "Run Python Code"
    nl_category = "Python"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Module")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Function")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Argument')
        self.inputs.new(NLValueFieldSocket.bl_idname, "Argument")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLParameterSocket.bl_idname, "Returned Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterPythonModuleFunction"

    def get_input_sockets_field_names(self):
        return ['condition', "module_name", "module_func", 'use_arg', 'arg']

    def get_output_socket_varnames(self):
        return ["OUT", "VAL"]


_nodes.append(NLParameterPythonModuleFunction)


class NLParameterBooleanValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterBooleanValue"
    bl_label = "Boolean"
    nl_category = "Values"
    nl_subcat = 'Simple'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "Bool")
        self.outputs.new(NLParameterSocket.bl_idname, "Bool")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]


_nodes.append(NLParameterBooleanValue)


class NLParameterFileValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterFileValue"
    bl_label = "File Path"
    nl_category = "Values"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFilePathSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Path")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterSimpleValue"

    def get_input_sockets_field_names(self):
        return ["value"]


_nodes.append(NLParameterFileValue)


class NLParameterFloatValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterFloatValue"
    bl_label = "Float"
    nl_category = "Values"
    nl_subcat = 'Simple'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Float")

    def get_netlogic_class_name(self): return "bgelogic.ParameterSimpleValue"
    def get_input_sockets_field_names(self): return ["value"]


_nodes.append(NLParameterFloatValue)


class NLParameterIntValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterIntValue"
    bl_label = "Integer"
    nl_category = "Values"
    nl_subcat = 'Simple'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Int")

    def get_netlogic_class_name(self): return "bgelogic.ParameterSimpleValue"
    def get_input_sockets_field_names(self): return ["value"]


_nodes.append(NLParameterIntValue)


class NLParameterStringValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterStringValue"
    bl_label = "String"
    nl_category = "Values"
    nl_subcat = 'Simple'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "String")

    def get_netlogic_class_name(self): return "bgelogic.ParameterSimpleValue"
    def get_input_sockets_field_names(self): return ["value"]


_nodes.append(NLParameterStringValue)


class NLParameterTypeCast(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterTypeCast"
    bl_label = "Typecast Value"
    nl_category = "Python"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLTypeCastSocket.bl_idname, '')
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterTypeCast"

    def get_input_sockets_field_names(self):
        return ['to_type', "value"]


_nodes.append(NLParameterTypeCast)


class NLParameterVector2SimpleNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterVector2SimpleNode"
    bl_label = "Vector 2"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLFloatFieldSocket, "X",
            NLFloatFieldSocket, "Y"
        )
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterVector2Simple"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y"]


_nodes.append(NLParameterVector2SimpleNode)


class NLParameterVector2SplitNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterVector2SplitNode"
    bl_label = "Separate XY"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLVec2FieldSocket, 'Vector'
        )
        self.outputs.new(NLFloatFieldSocket.bl_idname, "X")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Y")

    def get_netlogic_class_name(self): return "bgelogic.ParameterVector2Split"
    def get_output_socket_varnames(self): return ["OUTX", "OUTY"]
    def get_input_sockets_field_names(self): return ["input_v"]


_nodes.append(NLParameterVector2SplitNode)


class NLParameterVector3SplitNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterVector3SplitNode"
    bl_label = "Separate XYZ"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLVec3FieldSocket, 'Vector'
        )
        self.outputs.new(NLFloatFieldSocket.bl_idname, "X")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Y")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Z")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterVector3Split"

    def get_output_socket_varnames(self):
        return ["OUTX", "OUTY", 'OUTZ']

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLParameterVector3SplitNode)


class NLParameterAbsVector3Node(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterAbsVector3Node"
    bl_label = "Absolute Vector"
    nl_category = "Math"
    nl_subcat = 'Vector Math'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLVec3FieldSocket, 'Vector'
        )
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterAbsVector3"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_v"]


_nodes.append(NLParameterAbsVector3Node)


class NLParameterVector3SimpleNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterVector3SimpleNode"
    bl_label = "Vector 3"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLFloatFieldSocket, "X",
            NLFloatFieldSocket, "Y",
            NLFloatFieldSocket, "Z"
        )
        self.outputs.new(NLVectorSocket.bl_idname, "Vector")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterVector3Simple"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z"]


_nodes.append(NLParameterVector3SimpleNode)


class NLParameterRGBNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterRGBNode"
    bl_label = "Color RGB"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLSocketAlphaFloat, "R",
            NLSocketAlphaFloat, "G",
            NLSocketAlphaFloat, "B"
        )
        self.outputs.new(NLVectorSocket.bl_idname, "Color")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterVector3Simple"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z"]


_nodes.append(NLParameterRGBNode)


class NLParameterRGBANode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterRGBANode"
    bl_label = "Color RGBA"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "R")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "G")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "B")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "A")
        self.inputs[-1].value = 1
        self.outputs.new(NLVectorSocket.bl_idname, "Color")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterRGBA"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_r", "input_g", "input_b", 'input_a']


_nodes.append(NLParameterRGBANode)


class NLParameterEulerSimpleNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterEulerSimpleNode"
    bl_label = "Euler"
    nl_category = "Values"
    nl_subcat = 'Vectors'

    def init(self, context):
        NLParameterNode.init(self, context)
        tools.register_inputs(
            self,
            NLFloatFieldSocket, "X",
            NLFloatFieldSocket, "Y",
            NLFloatFieldSocket, "Z"
        )
        self.outputs.new(NLParameterSocket.bl_idname, "Euler")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterEulerSimple"

    def get_output_socket_varnames(self):
        return ["OUTV"]

    def get_input_sockets_field_names(self):
        return ["input_x", "input_y", "input_z"]


_nodes.append(NLParameterEulerSimpleNode)


class NLParameterEulerToMatrixNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterEulerToMatrixNode"
    bl_label = "Euler/Vector To Matrix"
    nl_category = "Math"
    nl_subcat = 'Vector Math'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, 'Euler')
        self.outputs.new(NLParameterSocket.bl_idname, "Matrix")

    def get_netlogic_class_name(self): return "bgelogic.ParameterEulerToMatrix"
    def get_output_socket_varnames(self): return ["OUT"]
    def get_input_sockets_field_names(self): return ["input_e"]


_nodes.append(NLParameterEulerToMatrixNode)


class NLParameterMatrixToEulerNode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterMatrixToEulerNode"
    bl_label = "Matrix To Euler"
    nl_category = "Math"
    nl_subcat = 'Vector Math'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, 'Matrix')
        self.outputs.new(NLParameterSocket.bl_idname, "Euler")

    def get_netlogic_class_name(self): return "bgelogic.ParameterMatrixToEuler"
    def get_output_socket_varnames(self): return ["OUT"]
    def get_input_sockets_field_names(self): return ["input_m"]


_nodes.append(NLParameterMatrixToEulerNode)


class NLOnInitConditionNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLOnInitConditionNode"
    bl_label = "On Init"
    bl_icon = 'SORTBYEXT'
    nl_category = "Events"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "Init")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionOnInit"

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self, cell_varname,
            uids,
            line_writer
        )


_nodes.append(NLOnInitConditionNode)


class NLOnUpdateConditionNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLOnUpdateConditionNode"
    bl_label = "On Update"
    nl_category = "Events"

    repeat: bpy.props.BoolProperty(update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.outputs.new(NLConditionSocket.bl_idname, "On Update")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionOnUpdate"

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )


_nodes.append(NLOnUpdateConditionNode)


class NLGamepadSticksCondition(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGamepadSticksCondition"
    bl_label = "Gamepad Sticks"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    axis: bpy.props.EnumProperty(
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, 'Inverted')
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, 'Index')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Sensitivity')
        self.inputs[-1].value = 1
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Threshold')
        self.inputs[-1].value = 0.05
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Left / Right")
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Up / Down")

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionGamepadSticks"

    def get_input_sockets_field_names(self):
        return ['inverted', "index", 'sensitivity', 'threshold']

    def get_output_socket_varnames(self):
        return ["X", "Y"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "axis", self.axis)


_nodes.append(NLGamepadSticksCondition)


class NLGamepadTriggerCondition(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGamepadTriggerCondition"
    bl_label = "Gamepad Trigger"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    axis: bpy.props.EnumProperty(
        items=_enum_controller_trigger_operators,
        description="Left or Right Trigger",
        update=update_tree_code
    )

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, 'Index')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Sensitivity')
        self.inputs[-1].value = 1
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Threshold')
        self.inputs[-1].value = 0.05
        self.outputs.new(NLFloatFieldSocket.bl_idname, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionGamepadTrigger"

    def get_input_sockets_field_names(self):
        return ["index", 'sensitivity', 'threshold']

    def get_output_socket_varnames(self):
        return ["VAL"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "axis", self.axis)


_nodes.append(NLGamepadTriggerCondition)


class NLGamepadButtonsCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLGamepadButtonsCondition"
    bl_label = "Gamepad Button"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    button: bpy.props.EnumProperty(
        name='Gamepad Buttons',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons",
        update=update_tree_code
    )
    pulse: bpy.props.BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_tree_code
    )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, 'Index')
        self.outputs.new(NLConditionSocket.bl_idname, "Is Pressed")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Down" if self.pulse else "Tap",
            toggle=True
        )
        layout.prop(self, "button", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionGamepadButtons"

    def get_input_sockets_field_names(self):
        return ["index"]

    def get_output_socket_varnames(self):
        return ["BUTTON"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer)
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            "pulse",
            self.pulse
        )
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            "button",
            self.button
        )


_nodes.append(NLGamepadButtonsCondition)


class NLKeyPressedCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLKeyPressedCondition"
    bl_label = "Key Down"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    pulse: bpy.props.BoolProperty(
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
        return "bgelogic.ConditionKeyPressed"

    def get_input_sockets_field_names(self):
        return ["key_code"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLKeyPressedCondition)


class NLKeyLoggerAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLKeyLoggerAction"
    bl_label = "Logger"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    pulse: bpy.props.BoolProperty(
        description=(
            'ON: True until the key is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
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
        return "bgelogic.ActionKeyLogger"

    def get_input_sockets_field_names(self):
        return ["condition"]

    def get_output_socket_varnames(self):
        return ["KEY_LOGGED", "KEY_CODE", "CHARACTER"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLKeyLoggerAction)


class NLKeyReleasedCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLKeyReleasedCondition"
    bl_label = "Key Up"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    pulse: bpy.props.BoolProperty(
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
        return "bgelogic.ConditionKeyReleased"

    def get_input_sockets_field_names(self):
        return ["key_code"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLKeyReleasedCondition)


class NLMousePressedCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLMousePressedCondition"
    bl_label = "Button"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    pulse: bpy.props.BoolProperty(
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
        return "bgelogic.ConditionMousePressed"

    def get_input_sockets_field_names(self):
        return ["mouse_button_code"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLMousePressedCondition)


class NLMouseMovedCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLMouseMovedCondition"
    bl_label = "Moved"
    bl_icon = 'MOUSE_MOVE'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    pulse: bpy.props.BoolProperty(
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
        return "bgelogic.ConditionMouseMoved"

    def get_input_sockets_field_names(self):
        return ["mouse_button_code"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLMouseMovedCondition)


class NLMouseReleasedCondition(bpy.types.Node, NLConditionNode):
    bl_idname = "NLMouseReleasedCondition"
    bl_label = "Button Up"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    pulse: bpy.props.BoolProperty(
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
        return "bgelogic.ConditionMouseReleased"

    def get_input_sockets_field_names(self):
        return ["mouse_button_code"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLMouseReleasedCondition)


class NLConditionOnceNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionOnceNode"
    bl_label = "Once"
    nl_category = "Events"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Repeat")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Reset After')
        self.inputs[-1].value = .5
        tools.register_outputs(self, NLConditionSocket, "Once")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionOnce"

    def get_input_sockets_field_names(self):
        return ["input_condition", 'repeat', 'reset_time']


_nodes.append(NLConditionOnceNode)


class NLObjectPropertyOperator(bpy.types.Node, NLConditionNode):
    bl_idname = "NLObjectPropertyOperator"
    bl_label = "Evaluate Property"
    bl_icon = 'CON_TRANSLIKE'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    operator: bpy.props.EnumProperty(
        items=_enum_logic_operators,
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self, cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            "operator",
            self.operator
        )

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'prop'
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'If True')
        self.outputs.new(NLParameterSocket.bl_idname, 'Value')

    def get_netlogic_class_name(self): return "bgelogic.ObjectPropertyOperator"

    def get_input_sockets_field_names(self):
        return [
            "game_object",
            "property_name",
            "compare_value"
        ]

    def get_output_socket_varnames(self):
        return [OUTCELL, "VAL"]


_nodes.append(NLObjectPropertyOperator)


class NLConditionNextFrameNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionNextFrameNode"
    bl_label = "On Next Frame"
    nl_category = "Events"

    def init(self, context):
        NLConditionNode.init(self, context)
        tools.register_inputs(self, NLPseudoConditionSocket, "Condition")
        tools.register_outputs(self, NLConditionSocket, "Next Frame")

    def get_netlogic_class_name(self):
        return "bgelogic.OnNextFrame"

    def get_input_sockets_field_names(self):
        return ["input_condition"]


_nodes.append(NLConditionNextFrameNode)


class NLConditionMousePressedOn(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionMousePressedOn"
    bl_label = "Button Over"
    bl_icon = 'MOUSE_LMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLMouseButtonSocket.bl_idname, "Mouse Button")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, "When Pressed On")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionMousePressedOn"

    def get_input_sockets_field_names(self):
        return ["mouse_button", "game_object"]


_nodes.append(NLConditionMousePressedOn)


class NLConditionMouseWheelMoved(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionMouseWheelMoved"
    bl_label = "Wheel"
    bl_icon = 'MOUSE_MMB'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLSocketMouseWheelDirection.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "When Scrolled")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionMouseScrolled"

    def get_input_sockets_field_names(self):
        return ["wheel_direction"]


_nodes.append(NLConditionMouseWheelMoved)


class NLConditionCollisionNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionCollisionNode"
    bl_label = "Collision"
    nl_category = "Physics"
    pulse: bpy.props.BoolProperty(
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.outputs.new(NLConditionSocket.bl_idname, "When Colliding")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Colliding Object")
        self.outputs.new(NLListSocket.bl_idname, "Colliding Objects")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Point")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Normal")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "pulse",
            text="Each Frame" if self.pulse else "Once",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionCollision"

    def get_input_sockets_field_names(self):
        return ["game_object", 'prop']

    def get_output_socket_varnames(self):
        return [OUTCELL, "TARGET", "OBJECTS", "POINT", "NORMAL"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line("{}.{} = {}", cell_varname, "pulse", self.pulse)


_nodes.append(NLConditionCollisionNode)


class NLConditionMouseTargetingNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionMouseTargetingNode"
    bl_label = "Over"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Enter")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Over")
        self.outputs.new(NLConditionSocket.bl_idname, "On Mouse Exit")
        self.outputs.new(NLParameterSocket.bl_idname, "Point")
        self.outputs.new(NLParameterSocket.bl_idname, "Normal")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionMouseTargeting"

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


class NLConditionAndNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionAndNode"
    bl_label = "And"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.outputs.new(NLConditionSocket.bl_idname, "If A and B")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionAnd"

    def get_input_sockets_field_names(self):
        return ["condition_a", "condition_b"]


_nodes.append(NLConditionAndNode)


class NLConditionAndNotNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionAndNotNode"
    bl_label = "And Not"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "A")
        self.inputs.new(NLConditionSocket.bl_idname, "B")
        self.outputs.new(NLConditionSocket.bl_idname, "If A and not B")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionAndNot"

    def get_input_sockets_field_names(self):
        return ["condition_a", "condition_b"]


_nodes.append(NLConditionAndNotNode)


class NLConditionOrNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionOrNode"
    bl_label = "Or"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'A')
        self.inputs.new(NLConditionSocket.bl_idname, 'B')
        self.outputs.new(NLConditionSocket.bl_idname, 'A or B')

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionOr"

    def get_input_sockets_field_names(self):
        return ["condition_a", "condition_b"]


_nodes.append(NLConditionOrNode)


class NLConditionOrList(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionOrList"
    bl_label = "Or List"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "A")
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "B")
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "C")
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "D")
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "E")
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "F")
        self.outputs.new(NLPseudoConditionSocket.bl_idname, "Or...")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionOrList"

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


class NLConditionAndList(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionAndList"
    bl_label = "And List"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "A")
        self.inputs[-1].default_value = True
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "B")
        self.inputs[-1].default_value = True
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "C")
        self.inputs[-1].default_value = True
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "D")
        self.inputs[-1].default_value = True
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "E")
        self.inputs[-1].default_value = True
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "F")
        self.inputs[-1].default_value = True
        self.outputs.new(NLPseudoConditionSocket.bl_idname, "If All True")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionAndList"

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


class NLConditionValueTriggerNode(bpy.types.Node, NLConditionNode):
    """When input becomes trigger, sends a true signal"""
    bl_idname = "NLConditionValueTriggerNode"
    bl_label = "On Value Changed To"
    nl_category = "Events"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value_type = "BOOLEAN"
        self.inputs[-1].value = "True"
        self.outputs.new(NLConditionSocket.bl_idname, "When Changed To")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionValueTrigger"

    def get_input_sockets_field_names(self):
        return ["monitored_value", "trigger_value"]


_nodes.append(NLConditionValueTriggerNode)


class NLConditionLogicOperation(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionLogicOperation"
    bl_label = "Compare"
    nl_category = "Math"
    operator: bpy.props.EnumProperty(
        items=_enum_logic_operators,
        update=update_tree_code
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Threshold")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "If True")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionLogicOp"

    def get_input_sockets_field_names(self):
        return ['threshold', "param_a", "param_b"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            "operator",
            self.operator
        )


_nodes.append(NLConditionLogicOperation)


class NLConditionCompareVecs(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionCompareVecs"
    bl_label = "Compare Vectors"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    operator: bpy.props.EnumProperty(
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
        return "bgelogic.ConditionCompareVecs"

    def get_input_sockets_field_names(self):
        return ['all', 'threshold', "param_a", "param_b"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            "operator",
            self.operator
        )


_nodes.append(NLConditionCompareVecs)


class NLConditionDistanceCheck(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionDistanceCheck"
    bl_label = "Check Distance"
    nl_category = "Math"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLSocketDistanceCheck.bl_idname, "Check")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "A")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "B")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Dist.")
        self.inputs.new(NLSocketOptionalPositiveFloat.bl_idname, "Hyst.")
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionDistanceCheck"

    def get_input_sockets_field_names(self):
        return ["operator", "param_a", "param_b", "dist", "hyst"]


_nodes.append(NLConditionDistanceCheck)


class NLConditionValueChanged(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionValueChanged"
    bl_label = "On Value Changed"
    nl_category = "Events"

    initialize: bpy.props.BoolProperty(
        description=(
            'When ON, skip the first change. '
            'When OFF, compare the first value to None'
        ),
        update=update_tree_code)

    def init(self, context):
        NLConditionNode.init(self, context)
        tools.register_inputs(self, NLParameterSocket, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If Changed")
        self.outputs.new(NLParameterSocket.bl_idname, "Old Value")
        self.outputs.new(NLParameterSocket.bl_idname, "New Value")

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "initialize",
            text="Skip Startup" if self.initialize else "On Startup",
            toggle=True
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionValueChanged"

    def get_input_sockets_field_names(self):
        return ["current_value"]

    def get_nonsocket_fields(self):
        return [("initialize", lambda: "True" if self.initialize else "False")]

    def get_output_socket_varnames(self):
        return [OUTCELL, "PREVIOUS_VALUE", "CURRENT_VALUE"]


_nodes.append(NLConditionValueChanged)


class NLConditionTimeElapsed(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionTimeElapsed"
    bl_label = "Timer"
    nl_category = 'Time'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "Repeat")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Seconds")
        self.outputs.new(NLConditionSocket.bl_idname, "When Elapsed")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionTimeElapsed"

    def get_input_sockets_field_names(self):
        return ["repeat", "delta_time"]


_nodes.append(NLConditionTimeElapsed)


class NLConditionNotNoneNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionNotNoneNode"
    bl_label = "Not None"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        tools.register_inputs(self, NLParameterSocket, "Value")
        tools.register_outputs(self, NLConditionSocket, "If Not None")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionNotNone"

    def get_input_sockets_field_names(self):
        return ["checked_value"]


_nodes.append(NLConditionNotNoneNode)


class NLConditionNoneNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionNone"
    bl_label = "None"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If None")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionNone"

    def get_input_sockets_field_names(self):
        return ["checked_value"]


_nodes.append(NLConditionNoneNode)


class NLConditionValueValidNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionValueValidNode"
    bl_label = "Value Valid"
    nl_category = "Values"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "If Valid")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionValueValid"

    def get_input_sockets_field_names(self):
        return ["checked_value"]


_nodes.append(NLConditionValueValidNode)


class NLConditionNotNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionNotNode"
    bl_label = "Not"
    nl_category = "Logic"

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, "If Not")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionNot"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLConditionNotNode)


class NLConditionLogicNetworkStatusNode(bpy.types.Node, NLConditionNode):
    bl_idname = "NLConditionLogitNetworkStatusNode"
    bl_label = "Logic Network Status"
    nl_category = "Logic"
    nl_subcat = 'Trees'

    def init(self, context):
        NLConditionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.outputs.new(NLConditionSocket.bl_idname, "If Running")
        self.outputs.new(NLConditionSocket.bl_idname, "If Stopped")

    def get_netlogic_class_name(self):
        return "bgelogic.ConditionLNStatus"

    def get_input_sockets_field_names(self):
        return ["game_object", "tree_name"]

    def get_output_socket_varnames(self):
        return ["IFRUNNING", "IFSTOPPED"]


_nodes.append(NLConditionLogicNetworkStatusNode)


class NLAddObjectActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLAddObjectActionNode"
    bl_label = "Add Object"
    bl_icon = 'PLUS'
    nl_category = "Objects"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectNameSocket.bl_idname, "Object to Add")
        self.inputs.new(
            NLGameObjectSocket.bl_idname,
            "Copy Data From (Optional)"
        )
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Life")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Added Object")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionAddObject"

    def get_input_sockets_field_names(self):
        return ["condition", "name", 'reference', "life"]

    def get_output_socket_varnames(self):
        return ['OUT', 'OBJ']


_nodes.append(NLAddObjectActionNode)


class NLSetGameObjectGamePropertyActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetGameObjectGamePropertyActionNode"
    bl_label = "Set Property"
    bl_icon = 'IMPORT'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetGameObjectGameProperty"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLSetGameObjectGamePropertyActionNode)


class NLSetMaterial(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetMaterial"
    bl_label = "Set Material"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Slot")
        self.inputs.new(NLMaterialSocket.bl_idname, "Material")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.SetMaterial"

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


class NLSetMaterialNodeValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetMaterialNodeValue"
    bl_label = "Set Node Input Value"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLMaterialSocket.bl_idname, 'Material')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Node Name")
        self.inputs[-1].value = 'Node'
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Input")
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Value')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetMaterialNodeValue"

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


class NLSetMaterialNodeInputValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetMaterialNodeInputValue"
    bl_label = "Set Input Value"
    nl_category = "Materials"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Input")
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Value')
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetMaterialNodeInputValue"

    def get_input_sockets_field_names(self):
        return ['condition', "input_slot", 'value']

    def get_output_socket_varnames(self):
        return ['OUT']


if not TOO_OLD:
    _nodes.append(NLSetMaterialNodeInputValue)


class NLToggleGameObjectGamePropertyActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLToggleGameObjectGamePropertyActionNode"
    bl_label = "Toggle Property"
    bl_icon = 'UV_SYNC_SELECT'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionToggleGameObjectGameProperty"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value"
        ]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLToggleGameObjectGamePropertyActionNode)


class NLAddToGameObjectGamePropertyActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLAddToGameObjectGamePropertyActionNode"
    bl_label = "Add To Property"
    bl_icon = 'ADD'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionAddToGameObjectGameProperty"

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


class NLCopyPropertyFromObject(bpy.types.Node, NLActionNode):
    bl_idname = "NLCopyPropertyFromObject"
    bl_label = "Copy From Object"
    bl_icon = 'PASTEDOWN'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Copy From")
        self.inputs.new(NLGameObjectSocket.bl_idname, "To")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.CopyPropertyFromObject"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "from_object",
            "to_object",
            "property_name"
        ]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLCopyPropertyFromObject)


class NLClampedModifyProperty(bpy.types.Node, NLActionNode):
    bl_idname = "NLClampedModifyProperty"
    bl_label = "Clamped Modify Property"
    bl_icon = 'ARROW_LEFTRIGHT'
    nl_category = "Objects"
    nl_subcat = 'Properties'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'prop'
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.inputs.new(NLVec2FieldSocket.bl_idname, "Range")
        self.outputs.new(NLConditionSocket.bl_idname, "Done")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionClampedAddToGameObjectGameProperty"

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


class NLValueSwitch(bpy.types.Node, NLParameterNode):
    bl_idname = "NLValueSwitch"
    bl_label = "Value Switch"
    nl_category = "Values"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "A if False, else B")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = 'A'
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.inputs[-1].value = 'B'
        self.outputs.new(NLParameterSocket.bl_idname, "A or B")

    def get_netlogic_class_name(self):
        return "bgelogic.ValueSwitch"

    def get_input_sockets_field_names(self):
        return ["condition", 'val_a', 'val_b']

    def get_output_socket_varnames(self):
        return ['VAL']


_nodes.append(NLValueSwitch)


class NLInvertBoolNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLInvertBoolNode"
    bl_label = "Invert Boolean"
    nl_category = "Values"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLBooleanSocket.bl_idname, "Bool")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.InvertBool"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLInvertBoolNode)


class NLInvertValueNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLInvertValueNode"
    bl_label = "Invert"
    nl_category = "Values"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.InvertValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLInvertValueNode)


class NLAbsoluteValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLAbsoluteValue"
    bl_label = "Absolute"
    nl_category = "Math"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_netlogic_class_name(self):
        return "bgelogic.AbsoluteValue"

    def get_input_sockets_field_names(self):
        return ["value"]

    def get_output_socket_varnames(self):
        return ['OUT']


_nodes.append(NLAbsoluteValue)


class NLCreateVehicleFromParent(bpy.types.Node, NLActionNode):
    bl_idname = "NLCreateVehicleFromParent"
    bl_label = "Create New Vehicle"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Car")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Suspension")
        self.inputs[-1].value = 0.06
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Stiffness")
        self.inputs[-1].value = 50
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Damping")
        self.inputs[-1].value = 5
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Friction")
        self.inputs[-1].value = 2
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Vehicle Constraint')
        self.outputs.new(NLListSocket.bl_idname, 'Wheels')

    def get_output_socket_varnames(self):
        return ["OUT", 'VEHICLE', 'WHEELS']

    def get_netlogic_class_name(self):
        return "bgelogic.ActionCreateVehicleFromParent"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            'suspension',
            'stiffness',
            'damping',
            'friction'
        ]


if not TOO_OLD:
    _nodes.append(NLCreateVehicleFromParent)


class NLVehicleApplyEngineForce(bpy.types.Node, NLActionNode):
    bl_idname = "NLVehicleApplyEngineForce"
    bl_label = "Accelerate"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    value_type: bpy.props.EnumProperty(
        items=_enum_vehicle_axis,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Vehicle Constraint")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Power")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.VehicleApplyForce"

    def get_input_sockets_field_names(self):
        return ["condition", "constraint", "wheelcount", 'power']

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = '{}'",
            cell_varname,
            "value_type",
            self.value_type
        )


if not TOO_OLD:
    _nodes.append(NLVehicleApplyEngineForce)


class NLVehicleApplyBraking(bpy.types.Node, NLActionNode):
    bl_idname = "NLVehicleApplyBraking"
    bl_label = "Brake"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    value_type: bpy.props.EnumProperty(
        items=_enum_vehicle_axis,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Vehicle Constraint")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Power")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.VehicleApplyBraking"

    def get_input_sockets_field_names(self):
        return ["condition", "constraint", "wheelcount", 'power']

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = '{}'",
            cell_varname,
            "value_type",
            self.value_type
        )


if not TOO_OLD:
    _nodes.append(NLVehicleApplyBraking)


class NLVehicleApplySteering(bpy.types.Node, NLActionNode):
    bl_idname = "NLVehicleApplySteering"
    bl_label = "Steer"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    value_type: bpy.props.EnumProperty(
        items=_enum_vehicle_axis,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Vehicle Constraint")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Wheels")
        self.inputs[-1].value = 2
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Steer")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.VehicleApplySteering"

    def get_input_sockets_field_names(self):
        return ["condition", "constraint", "wheelcount", 'power']

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = '{}'",
            cell_varname,
            "value_type",
            self.value_type
        )


if not TOO_OLD:
    _nodes.append(NLVehicleApplySteering)


class NLVehicleSetAttributes(bpy.types.Node, NLActionNode):
    bl_idname = "NLVehicleSetAttributes"
    bl_label = "Set Attributes"
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    value_type: bpy.props.EnumProperty(
        items=_enum_vehicle_axis,
        update=update_tree_code
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Vehicle Constraint")
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

    def get_output_socket_varnames(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_netlogic_class_name(self):
        return "bgelogic.VehicleSetAttributes"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "constraint",
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

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = '{}'",
            cell_varname,
            "value_type",
            self.value_type
        )


if not TOO_OLD:
    _nodes.append(NLVehicleSetAttributes)


class NLSetObjectAttributeActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetObjectAttributeActionNode"
    bl_label = "Set Position / Rotation / Scale etc."
    bl_icon = 'VIEW3D'
    nl_category = "Objects"
    nl_subcat = 'Data'
    value_type: bpy.props.EnumProperty(
        items=_enum_writable_member_names,
        update=update_tree_code,
        default='worldPosition'
    )

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
        return "bgelogic.ActionSetObjectAttribute"

    def get_input_sockets_field_names(self):
        return ["condition", "xyz", "game_object", "attribute_value"]

    def init_cell_fields(self, cell_varname, uids, line_writer):
        NetLogicStatementGenerator.init_cell_fields(
            self,
            cell_varname,
            uids,
            line_writer
        )
        line_writer.write_line(
            "{}.{} = '{}'",
            cell_varname,
            "value_type",
            self.value_type
        )


_nodes.append(NLSetObjectAttributeActionNode)


class NLActionRayCastNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRayCastNode"
    bl_label = "Ray"
    nl_category = "Ray Casts"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Origin")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Destination")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Property")
        self.inputs.new(NLBooleanSocket.bl_idname, 'X-Ray')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Distance")
        self.inputs[-1].value = 100.0
        self.outputs.new(NLConditionSocket.bl_idname, "Has Result")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Picked Object")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Point")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Picked Normal")
        self.outputs.new(NLVec3FieldSocket.bl_idname, "Ray Direction")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRayPick"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "origin",
            "destination",
            "property_name",
            'xray',
            "distance"
        ]

    def get_output_socket_varnames(self):
        return [OUTCELL, "PICKED_OBJECT", "POINT", "NORMAL", "DIRECTION"]


_nodes.append(NLActionRayCastNode)


# TODO: should we reset conditions that have been consumed?
# Like a "once" condition. I'd say no.
class NLStartLogicNetworkActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLStartLogicNetworkActionNode"
    bl_label = "Start Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLSocketLogicTree.bl_idname, 'Tree Name')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStartLogicNetwork"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "logic_network_name"]


_nodes.append(NLStartLogicNetworkActionNode)


class NLStopLogicNetworkActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLStopLogicNetworkActionNode"
    bl_label = "Stop Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.inputs.new(NLSocketLogicTree.bl_idname, 'Tree Name')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStopLogicNetwork"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "logic_network_name"]


_nodes.append(NLStopLogicNetworkActionNode)


class NLActionSetGameObjectVisibility(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetGameObjectVisibility"
    bl_label = "Set Visibility"
    bl_icon = 'HIDE_OFF'
    nl_category = "Objects"

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
        return "bgelogic.ActionSetGameObjectVisibility"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "visible", "recursive"]


_nodes.append(NLActionSetGameObjectVisibility)


class NLActionFindObjectNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionFindObjectNode"
    bl_label = "Get Object"
    bl_icon = 'OBJECT_DATA'
    nl_category = "Objects"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Object")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionFindObject"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_output_socket_varnames(self):
        return [OUTCELL]


_nodes.append(NLActionFindObjectNode)


class NLActionSetActiveCamera(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetActiveCamera"
    bl_label = "Set Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Camera')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetActiveCamera"

    def get_input_sockets_field_names(self):
        return ["condition", "camera"]


_nodes.append(NLActionSetActiveCamera)


class NLActionSetCameraFov(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetCameraFov"
    bl_label = "Set FOV"
    nl_category = "Scene"
    nl_subcat = 'Camera'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Camera')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'FOV')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetCameraFov"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", 'fov']


_nodes.append(NLActionSetCameraFov)


class NLActionSetResolution(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetResolution"
    bl_label = "Set Resolution"
    nl_category = 'Render'

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
        return "bgelogic.ActionSetResolution"

    def get_input_sockets_field_names(self):
        return ["condition", "x_res", 'y_res']


_nodes.append(NLActionSetResolution)


class NLActionSetFullscreen(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetFullscreen"
    bl_label = "Set Fullscreen"
    nl_category = 'Render'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Fullscreen')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetFullscreen"

    def get_input_sockets_field_names(self):
        return ["condition", "use_fullscreen"]


_nodes.append(NLActionSetFullscreen)


class NLActionSetVSync(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetVSync"
    bl_label = "Set VSync"
    nl_category = 'Render'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLVSyncSocket.bl_idname, 'Vsync')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetVSync"

    def get_input_sockets_field_names(self):
        return ["condition", "vsync_mode"]


_nodes.append(NLActionSetVSync)


class NLInitEmptyDict(bpy.types.Node, NLActionNode):
    bl_idname = "NLInitEmptyDict"
    bl_label = "Init Empty"
    nl_category = "Python"
    nl_subcat = 'Dictionary'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
        return ["OUT", 'DICT']

    def get_netlogic_class_name(self):
        return "bgelogic.InitEmptyDict"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLInitEmptyDict)


class NLInitNewDict(bpy.types.Node, NLActionNode):
    bl_idname = "NLInitNewDict"
    bl_label = "Init From Item"
    nl_category = "Python"
    nl_subcat = 'Dictionary'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Key')
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
        return ["OUT", 'DICT']

    def get_netlogic_class_name(self):
        return "bgelogic.InitNewDict"

    def get_input_sockets_field_names(self):
        return ["condition", 'key', 'val']


_nodes.append(NLInitNewDict)


class NLSetDictKeyValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetDictKeyValue"
    bl_label = "Set Key"
    nl_category = "Python"
    nl_subcat = 'Dictionary'

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
        return "bgelogic.SetDictKeyValue"

    def get_input_sockets_field_names(self):
        return ["condition", 'dict', 'key', 'val']


_nodes.append(NLSetDictKeyValue)


class NLSetDictDelKey(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetDictDelKey"
    bl_label = "Remove Key"
    nl_category = "Python"
    nl_subcat = 'Dictionary'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLDictSocket.bl_idname, 'Dictionary')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Key')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Dictionary')

    def get_output_socket_varnames(self):
        return ["OUT", "DICT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetDictDelKey"

    def get_input_sockets_field_names(self):
        return ["condition", 'dict', 'key']


_nodes.append(NLSetDictDelKey)


class NLInitEmptyList(bpy.types.Node, NLActionNode):
    bl_idname = "NLInitEmptyList"
    bl_label = "Init Empty"
    nl_category = "Python"
    nl_subcat = 'List'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLIntegerFieldSocket.bl_idname, 'Length')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ["OUT", 'LIST']

    def get_netlogic_class_name(self):
        return "bgelogic.InitEmptyList"

    def get_input_sockets_field_names(self):
        return ["condition", 'length']


_nodes.append(NLInitEmptyList)


class NLInitNewList(bpy.types.Node, NLActionNode):
    bl_idname = "NLInitNewList"
    bl_label = "From Items"
    nl_category = "Python"
    nl_subcat = 'List'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 1')
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 2')
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 3')
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 4')
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 5')
        self.inputs.new(NLParameterSocket.bl_idname, 'Item 6')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def get_output_socket_varnames(self):
        return ['LIST']

    def get_netlogic_class_name(self):
        return "bgelogic.InitNewList"

    def get_input_sockets_field_names(self):
        return [
            'value',
            'value2',
            'value3',
            'value4',
            'value5',
            'value6'
        ]


_nodes.append(NLInitNewList)


class NLAppendListItem(bpy.types.Node, NLActionNode):
    bl_idname = "NLAppendListItem"
    bl_label = "Append"
    nl_category = "Python"
    nl_subcat = 'List'

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
        return "bgelogic.AppendListItem"

    def get_input_sockets_field_names(self):
        return ["condition", 'list', 'val']


_nodes.append(NLAppendListItem)


class NLSetListIndex(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetListIndex"
    bl_label = "Set Index"
    nl_category = "Python"
    nl_subcat = 'List'

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
        return "bgelogic.SetListIndex"

    def get_input_sockets_field_names(self):
        return ["condition", 'list', 'index', 'val']


_nodes.append(NLSetListIndex)


class NLRemoveListValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLRemoveListValue"
    bl_label = "Remove Value"
    nl_category = "Python"
    nl_subcat = 'List'

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
        return "bgelogic.RemoveListValue"

    def get_input_sockets_field_names(self):
        return ["condition", 'list', 'val']


_nodes.append(NLRemoveListValue)


class NLActionInstallSubNetwork(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionInstallSubNetwork"
    bl_label = "Add Logic Tree to Object"
    nl_category = "Logic"
    nl_subcat = 'Trees'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.inputs.new(NLBooleanSocket.bl_idname, "Enabled")
        self.inputs[-1].use_toggle = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionInstalSubNetwork"

    def get_input_sockets_field_names(self):
        return ["condition", "target_object", "tree_name", "initial_status"]


_nodes.append(NLActionInstallSubNetwork)


class NLActionExecuteNetwork(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionExecuteNetwork"
    bl_label = "Execute Logic Tree"
    nl_category = "Logic"
    nl_subcat = 'Trees'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target Object")
        self.inputs.new(NLSocketLogicTree.bl_idname, "Tree Name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionExecuteNetwork"

    def get_input_sockets_field_names(self):
        return ["condition", "target_object", "tree_name"]


_nodes.append(NLActionExecuteNetwork)


class NLActionStopAnimation(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStopAnimation"
    bl_label = "Stop Animation"
    nl_category = "Animation"

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
        return "bgelogic.ActionStopAnimation"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "action_layer"]


_nodes.append(NLActionStopAnimation)


class NLActionSetAnimationFrame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetAnimationFrame"
    bl_label = "Set Animation Frame"
    nl_category = "Animation"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLAnimationSocket.bl_idname, "Action")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Frame")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Layer Weight")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetAnimationFrame"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "action_layer",
            "action_frame",
            'layer_weight'
        ]


_nodes.append(NLActionSetAnimationFrame)


class NLActionApplyLocation(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionApplyLocation"
    bl_label = "Apply Movement"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    local: bpy.props.BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        tools.register_inputs(
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
            text="Apply Local" if self.local else "Apply Global"
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ActionApplyLocation"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "movement"]

    def get_nonsocket_fields(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyLocation)


class NLActionApplyRotation(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionApplyRotation"
    bl_label = "Apply Rotation"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    local: bpy.props.BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        tools.register_inputs(
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
            text="Apply Local" if self.local else "Apply Global"
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ActionApplyRotation"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "rotation"]

    def get_nonsocket_fields(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyRotation)


class NLActionApplyForce(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionApplyForce"
    bl_label = "Apply Force"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    local: bpy.props.BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        tools.register_inputs(
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
            text="Apply Local" if self.local else "Apply Global"
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ActionApplyForce"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "force"]

    def get_nonsocket_fields(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyForce)


class NLActionApplyImpulse(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionApplyImpulse"
    bl_label = "Apply Impulse"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    local: bpy.props.BoolProperty(default=False, update=update_tree_code)

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
            text="Apply Local" if self.local else "Apply Global"
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ActionApplyImpulse"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "point", 'impulse']

    def get_nonsocket_fields(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyImpulse)


class NLActionCharacterJump(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionCharacterJump"
    bl_label = "Jump"
    nl_category = "Physics"
    nl_subcat = 'Character'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Object')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionCharacterJump"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object"]


_nodes.append(NLActionCharacterJump)


class NLActionSaveGame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSaveGame"
    bl_label = "Save Game"
    bl_icon = 'FILE_TICK'
    nl_category = "Game"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        return "bgelogic.ActionSaveGame"

    def get_input_sockets_field_names(self):
        return ["condition", 'slot']

    def get_nonsocket_fields(self):
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


class NLActionLoadGame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionLoadGame"
    bl_label = "Load Game"
    nl_category = "Game"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        return "bgelogic.ActionLoadGame"

    def get_input_sockets_field_names(self):
        return ["condition", 'slot']

    def get_nonsocket_fields(self):
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


class NLActionSaveVariable(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSaveVariable"
    bl_label = "Save Variable"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'var'
        self.inputs.new(NLValueFieldSocket.bl_idname, '')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.label(text='Save To:')
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
        return "bgelogic.ActionSaveVariable"

    def get_input_sockets_field_names(self):
        return ["condition", 'name', 'val']

    def get_nonsocket_fields(self):
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


class NLActionSaveVariables(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSaveVariables"
    bl_label = "Save Variable Dict"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        self.inputs.new(NLDictSocket.bl_idname, 'Variables')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.label(text='Save To:')
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
        return "bgelogic.ActionSaveVariables"

    def get_input_sockets_field_names(self):
        return ["condition", 'val']

    def get_nonsocket_fields(self):
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


class NLParameterSetAttribute(bpy.types.Node, NLActionNode):
    bl_idname = "NLParameterSetAttribute"
    bl_label = "Set Object Attribute"
    nl_category = "Python"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPythonSocket.bl_idname, "Object Instance")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Attribute")
        self.inputs.new(NLValueFieldSocket.bl_idname, "")

    def get_netlogic_class_name(self):
        return "bgelogic.setObInstanceAttr"

    def get_input_sockets_field_names(self):
        return ['instance', 'attr', 'value']


_nodes.append(NLParameterSetAttribute)


class NLActionLoadVariable(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionLoadVariable"
    bl_label = "Load Variable"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'var'
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Value')

    def draw_buttons(self, context, layout):
        layout.label(text='Load From:')
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
        return "bgelogic.ActionLoadVariable"

    def get_input_sockets_field_names(self):
        return ["condition", 'name']

    def get_nonsocket_fields(self):
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
        return ["OUT", "VAR"]


_nodes.append(NLActionLoadVariable)


class NLActionLoadVariables(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionLoadVariables"
    bl_label = "Load Variable Dict"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLDictSocket.bl_idname, 'Variables')

    def draw_buttons(self, context, layout):
        layout.label(text='Load From:')
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
        return "bgelogic.ActionLoadVariables"

    def get_input_sockets_field_names(self):
        return ["condition", 'name']

    def get_nonsocket_fields(self):
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
        return ["OUT", "VAR"]


_nodes.append(NLActionLoadVariables)


class NLActionRemoveVariable(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRemoveVariable"
    bl_label = "Remove Variable"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs[-1].value = 'var'
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.label(text='Remove From:')
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
        return "bgelogic.ActionRemoveVariable"

    def get_input_sockets_field_names(self):
        return ["condition", 'name']

    def get_nonsocket_fields(self):
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


class NLActionClearVariables(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionClearVariables"
    bl_label = "Clear Variables"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
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
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def draw_buttons(self, context, layout):
        layout.label(text='Clear In:')
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
        return "bgelogic.ActionClearVariables"

    def get_input_sockets_field_names(self):
        return ["condition"]

    def get_nonsocket_fields(self):
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


class NLActionListVariables(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionListVariables"
    bl_label = "List Saved Variables"
    nl_category = "Variables"
    custom_path: bpy.props.BoolProperty(update=update_tree_code)
    path: bpy.props.StringProperty(
        subtype='FILE_PATH',
        update=update_tree_code,
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Print')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLListSocket.bl_idname, 'List')

    def draw_buttons(self, context, layout):
        layout.label(text='List From:')
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
        return "bgelogic.ActionListVariables"

    def get_input_sockets_field_names(self):
        return ["condition", 'print_list']

    def get_nonsocket_fields(self):
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


class NLActionSetCharacterJump(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetActionCharacterJump"
    bl_label = "Set Max Jumps"
    nl_category = "Physics"
    nl_subcat = 'Character'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Max Jumps")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetCharacterJump"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'max_jumps']


_nodes.append(NLActionSetCharacterJump)


class NLActionSetCharacterGravity(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetCharacterGravity"
    bl_label = "Set Gravity"
    nl_category = "Physics"
    nl_subcat = 'Character'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Gravity")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetCharacterGravity"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'gravity']


_nodes.append(NLActionSetCharacterGravity)


class NLActionSetCharacterWalkDir(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetCharacterWalkDir"
    bl_label = "Set Walk Direction"
    nl_category = "Physics"
    nl_subcat = 'Character'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetCharacterWalkDir"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", 'walkDir']


_nodes.append(NLActionSetCharacterWalkDir)


class NLActionGetCharacterInfo(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionGetCharacterInfo"
    bl_label = "Get Physics Info"
    nl_category = "Physics"
    nl_subcat = 'Character'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLIntegerFieldSocket.bl_idname, 'Max Jumps')
        self.outputs.new(NLIntegerFieldSocket.bl_idname, 'Active Jump Count')
        self.outputs.new(NLFloatFieldSocket.bl_idname, 'Gravity')
        self.outputs.new(NLBooleanSocket.bl_idname, 'On Ground')

    def get_netlogic_class_name(self):
        return "bgelogic.ActionGetCharacterInfo"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object"]

    def get_output_socket_varnames(self):
        return ["MAX_JUMPS", "CUR_JUMP", "GRAVITY", 'ON_GROUND']


_nodes.append(NLActionGetCharacterInfo)


class NLActionApplyTorque(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionApplyTorque"
    bl_label = "Apply Torque"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    local: bpy.props.BoolProperty(default=True, update=update_tree_code)

    def init(self, context):
        NLActionNode.init(self, context)
        tools.register_inputs(
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
            text="Apply Local" if self.local else "Apply Global"
        )

    def get_netlogic_class_name(self):
        return "bgelogic.ActionApplyTorque"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "torque"]

    def get_nonsocket_fields(self):
        return [("local", lambda: "True" if self.local else "False")]


_nodes.append(NLActionApplyTorque)


class NLActionEndObjectNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionEndObjectNode"
    bl_label = "Remove Object"
    bl_icon = 'TRASH'
    nl_category = "Objects"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionEndObject"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object"]


_nodes.append(NLActionEndObjectNode)


class NLActionSetTimeScale(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetTimeScale"
    bl_label = "Set Timescale"
    nl_category = "Scene"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Timescale")
        self.inputs[-1].value = 1
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetTimeScale"

    def get_input_sockets_field_names(self):
        return ["condition", "timescale"]


_nodes.append(NLActionSetTimeScale)


class NLActionSetGravity(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetGravity"
    bl_label = "Set Gravity"
    nl_category = "Scene"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Gravity")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self): return "bgelogic.ActionSetGravity"
    def get_input_sockets_field_names(self): return ["condition", "gravity"]


_nodes.append(NLActionSetGravity)


class NLActionReplaceMesh(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionReplaceMesh"
    bl_label = "Replace Mesh"
    bl_icon = 'MESH_DATA'
    nl_category = "Objects"
    nl_subcat = 'Data'

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
        return "bgelogic.ActionReplaceMesh"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "target_game_object",
            "new_mesh_name",
            "use_display",
            "use_physics"
        ]


_nodes.append(NLActionReplaceMesh)


class NLActionRemovePhysicsConstraint(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRemovePhysicsConstraint"
    bl_label = "Remove Constraint"
    bl_icon = 'TRASH'
    nl_category = "Physics"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.RemovePhysicsConstraint"

    def get_input_sockets_field_names(self):
        return ["condition", "object", "name"]


_nodes.append(NLActionRemovePhysicsConstraint)


class NLActionAddPhysicsConstraint(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionAddPhysicsConstraint"
    bl_label = "Add Constraint"
    bl_icon = 'CONSTRAINT'
    nl_category = "Physics"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Target")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, 'Name')
        self.inputs.new(NLConstraintTypeSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use World Space')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Pivot')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Limit Axis')
        self.inputs.new(NLVec3FieldSocket.bl_idname, 'Axis Limits')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Linked Collision')
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.AddPhysicsConstraint"

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


class NLSetGammaAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetGammaAction"
    bl_label = "Set Gamma"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Gamma')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetGamma"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetGammaAction)


class NLSetExposureAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetExposureAction"
    bl_label = "Set Exposure"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLPositiveFloatSocket.bl_idname, 'Exposure')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetExposure"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetExposureAction)


class NLSetEeveeBloom(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetEeveeBloom"
    bl_label = "Set Bloom"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Bloom')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetEeveeBloom"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetEeveeBloom)


class NLSetEeveeSSR(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetEeveeSSR"
    bl_label = "Set SSR"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use SSR')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetEeveeSSR"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetEeveeSSR)


class NLSetEeveeVolumetrics(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetEeveeVolumetrics"
    bl_label = "Set Volumetric Light"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Volumetrics')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetEeveeVolumetrics"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetEeveeVolumetrics)


class NLSetEeveeVolumetricShadows(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetEeveeVolumetricShadows"
    bl_label = "Set Volumetric Shadows"
    nl_category = 'Render'
    nl_subcat = 'Visuals'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Vol. Shadows')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetEeveeVolumetricShadows"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "value"
        ]


if not TOO_OLD:
    _nodes.append(NLSetEeveeVolumetricShadows)


class NLSetLightEnergyAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetLightEnergyAction"
    bl_label = "Set Light Energy"
    nl_category = "Lights"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Light Object')
        self.inputs.new(NLFloatFieldSocket.bl_idname, 'Energy')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetLightEnergy"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "lamp",
            "energy"
        ]


_nodes.append(NLSetLightEnergyAction)


class NLSetLightShadowAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetLightShadowAction"
    bl_label = "Set Light Shadow"
    nl_category = "Lights"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, 'Condition')
        self.inputs.new(NLGameObjectSocket.bl_idname, 'Light Object')
        self.inputs.new(NLBooleanSocket.bl_idname, 'Use Shadow')
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetLightShadow"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "lamp",
            "use_shadow"
        ]


_nodes.append(NLSetLightShadowAction)


class NLSetLightColorAction(bpy.types.Node, NLActionNode):
    bl_idname = "NLSetLightColorAction"
    bl_label = "Set Light Color"
    bl_icon = 'COLOR'
    nl_category = "Lights"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Light Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Clamp")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Red")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Green")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Blue")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.SetLightColor"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "lamp",
            'clamp',
            "red",
            "green",
            "blue"
        ]


_nodes.append(NLSetLightColorAction)


class NLGetLightEnergy(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetLightEnergy"
    bl_label = "Get Light Energy"
    nl_category = "Lights"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Light Object")
        self.outputs.new(NLParameterSocket.bl_idname, 'Enery')

    def get_output_socket_varnames(self):
        return ['ENERGY']

    def get_netlogic_class_name(self):
        return "bgelogic.GetLightEnergy"

    def get_input_sockets_field_names(self):
        return ["lamp"]


_nodes.append(NLGetLightEnergy)


class NLGetLightColorAction(bpy.types.Node, NLParameterNode):
    bl_idname = "NLGetLightColorAction"
    bl_label = "Get Light Color"
    nl_category = "Lights"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Light Object")
        self.outputs.new(NLParameterSocket.bl_idname, 'Red')
        self.outputs.new(NLParameterSocket.bl_idname, 'Green')
        self.outputs.new(NLParameterSocket.bl_idname, 'Blue')

    def get_output_socket_varnames(self):
        return ['R', 'G', 'B']

    def get_netlogic_class_name(self):
        return "bgelogic.GetLightColor"

    def get_input_sockets_field_names(self):
        return ["lamp"]


_nodes.append(NLGetLightColorAction)


class NLActionPlayActionNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionPlayActionNode"
    bl_label = "Play Animation"
    nl_category = "Animation"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object / Armature")
        self.inputs.new(NLAnimationSocket.bl_idname, "Action")
        self.inputs.new(NLBooleanSocket.bl_idname, "Stop When Done")
        self.inputs[-1].value = True
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Start Frame")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "End Frame")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Layer")
        self.inputs.new(NLPositiveIntegerFieldSocket.bl_idname, "Priority")
        self.inputs.new(NLPlayActionModeSocket.bl_idname, "Play Mode")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Layer Weight")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Speed")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Blendin")
        self.inputs.new(NLBlendActionModeSocket.bl_idname, "Blend Mode")
        self.outputs.new(NLConditionSocket.bl_idname, "Started")
        self.outputs.new(NLConditionSocket.bl_idname, "Running")
        self.outputs.new(NLConditionSocket.bl_idname, "Finished")
        self.outputs.new(NLParameterSocket.bl_idname, "Current Frame")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionPlayAction"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "stop",
            "start_frame",
            "end_frame",
            "layer",
            "priority",
            "play_mode",
            "layer_weight",
            "speed",
            "blendin",
            "blend_mode"
        ]

    def get_output_socket_varnames(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]


_nodes.append(NLActionPlayActionNode)


class NLActionLibLoadNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionLibLoadNode"
    bl_label = "Load Blender File"
    nl_category = "Game"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFilePathSocket.bl_idname, "Path")
        self.outputs.new(NLConditionSocket.bl_idname, "When Loaded")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionLibLoad"

    def get_input_sockets_field_names(self):
        return ["condition", "path"]


_nodes.append(NLActionLibLoadNode)


class NLActionLibFreeNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionLibFreeNode"
    bl_label = "Unload Blender File"
    nl_category = "Game"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFilePathSocket.bl_idname, "Path")
        self.outputs.new(NLConditionSocket.bl_idname, "When Unloaded")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionLibFree"

    def get_input_sockets_field_names(self):
        return ["condition", "path"]


_nodes.append(NLActionLibFreeNode)


class NLActionAlignAxisToVector(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionAlignAxisToVector"
    bl_label = "Align Axis to Vector"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Vector")
        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Axis")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Factor")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionAlignAxisToVector"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "vector", "axis", "factor"]


_nodes.append(NLActionAlignAxisToVector)


# If the condition stays true for N seconds, do something,
# then wait N seconds to repeat
class NLActionTimeBarrier(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionTimeBarrier"
    bl_label = "Time Barrier"
    nl_category = 'Time'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Delay Sec.")
        self.inputs.new(NLBooleanSocket.bl_idname, "Repeat")
        self.inputs[-1].use_toggle = True
        self.inputs[-1].true_label = "Repeat"
        self.inputs[-1].false_label = "Once"
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionTimeBarrier"

    def get_input_sockets_field_names(self):
        return ["condition", "delay", "repeat"]


_nodes.append(NLActionTimeBarrier)


class NLActionTimeDelay(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionTimeDelay"
    bl_label = "Delay"
    bl_icon = 'PREVIEW_RANGE'
    nl_category = "Time"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Delay Sec.")
        self.inputs.new(NLBooleanSocket.bl_idname, "Repeat")
        self.inputs[-1].use_toggle = True
        self.inputs[-1].true_label = "Repeat"
        self.inputs[-1].false_label = "Do not repeat"
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionTimeDelay"

    def get_input_sockets_field_names(self):
        return ["condition", "delay", "repeat"]


_nodes.append(NLActionTimeDelay)


# When the condition is True,
# set to True then do the next check only after
# N seconds have elapsed
class NLActionTimeFilter(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionTimeFilter"
    bl_label = "Time Filter"
    bl_icon = 'TEMP'
    nl_category = "Time"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Delay Sec.")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, "Out")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionTimeFilter"

    def get_input_sockets_field_names(self):
        return ["condition", "delay"]


_nodes.append(NLActionTimeFilter)


class NLActionMouseLookNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionMouseLookNode"
    bl_label = "Look"
    bl_icon = 'CAMERA_DATA'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Main Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Head (Optional)")
        self.inputs.new(NLInvertedXYSocket.bl_idname, "")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Sensitivity")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLBooleanSocket.bl_idname, "Cap Left / Right")
        self.inputs.new(NLVec2PositiveFieldSocket.bl_idname, "")
        self.inputs.new(NLBooleanSocket.bl_idname, "Cap Up / Down")
        self.inputs.new(NLVec2PositiveFieldSocket.bl_idname, "")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Smoothing")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionMouseLook"

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


class NLActionPrint(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionPrint"
    bl_label = "Print"
    bl_icon = 'CONSOLE'
    nl_category = "Utilities"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Value")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionPrint"

    def get_input_sockets_field_names(self):
        return ["condition", "value"]


_nodes.append(NLActionPrint)


class NLActionResetTaaSamples(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionResetTaaSamples"
    bl_label = "Reset TAA Samples"
    bl_icon = 'FILE_REFRESH'
    nl_category = 'Render'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionResetTaaSamples"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLActionResetTaaSamples)


class NLActionMousePickNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionMousePickNode"
    bl_label = "Mouse Ray"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Ray Casts"

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
        return "bgelogic.ActionMousePick"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", "property", 'xray', "distance"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "OUTOBJECT", "OUTPOINT", "OUTNORMAL"]


_nodes.append(NLActionMousePickNode)


class NLActionCameraPickNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionCameraPickNode"
    bl_label = "Camera Ray"
    bl_icon = 'CAMERA_DATA'
    nl_category = "Ray Casts"

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
        return "bgelogic.ActionCameraPick"

    def get_input_sockets_field_names(self):
        return ["condition", "camera", "aim", "property_name", "xray", "distance"]

    def get_output_socket_varnames(self):
        return [OUTCELL, "PICKED_OBJECT", "PICKED_POINT", "PICKED_NORMAL"]


_nodes.append(NLActionCameraPickNode)


class NLActionSetParentNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetParentNode"
    bl_label = "Set Parent"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Parent Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Compound")
        self.inputs[-1].value = True
        self.inputs.new(NLBooleanSocket.bl_idname, "Ghost")
        self.inputs[-1].value = True
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetParent"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "child_object",
            "parent_object",
            "compound",
            "ghost"
        ]


_nodes.append(NLActionSetParentNode)


class NLActionRemoveParentNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRemoveParentNode"
    bl_label = "Remove Parent"
    bl_icon = 'X'
    nl_category = "Objects"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRemoveParent"

    def get_input_sockets_field_names(self):
        return ["condition", "child_object"]


_nodes.append(NLActionRemoveParentNode)


class NLActionGetPerformanceProfileNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionGetPerformanceProfileNode"
    bl_label = "Get Profile"
    bl_icon = 'TEXT'
    nl_category = "Utilities"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Print Profile")
        self.inputs.new(NLBooleanSocket.bl_idname, "Evaluated Nodes")
        self.inputs.new(NLBooleanSocket.bl_idname, "Nodes per Second")
        self.inputs.new(NLBooleanSocket.bl_idname, "Nodes per Tick")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Profile')

    def get_output_socket_varnames(self):
        return ["OUT", "DATA"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionPerformanceProfile"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "print_profile",
            "check_evaluated_cells",
            'check_average_cells_per_sec',
            'check_cells_per_tick'
        ]


_nodes.append(NLActionGetPerformanceProfileNode)


class NLParameterGameObjectParent(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterGameObjectParent"
    bl_label = "Get Parent"
    bl_icon = 'COMMUNITY'
    nl_category = "Objects"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLGameObjectSocket.bl_idname, "Child Object")
        self.outputs.new(NLGameObjectSocket.bl_idname, "Parent Object")

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterParentGameObject"

    def get_input_sockets_field_names(self):
        return ["game_object"]


_nodes.append(NLParameterGameObjectParent)


class NLParameterAxisVector(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterAxisVector"
    bl_label = "Get Axis Vector"
    bl_icon = 'EMPTY_ARROWS'
    nl_category = "Objects"
    nl_subcat = 'Data'
    axis: bpy.props.EnumProperty(
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
        return "bgelogic.ParameterAxisVector"

    def get_input_sockets_field_names(self):
        return ["game_object"]

    def get_nonsocket_fields(self):
        return [("axis", lambda: self.axis)]


_nodes.append(NLParameterAxisVector)


class NLActionEditArmatureConstraint(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionEditArmatureConstraint"
    bl_label = "Edit Armature Constraint"
    bl_icon = 'CONSTRAINT_BONE'
    nl_category = "Animation"
    nl_subcat = 'Armature / Rig'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Constraint Name")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "Enforced Factor")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Primary Target")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Secondary Target")
        self.inputs.new(NLBooleanSocket.bl_idname, "Active")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "IK Weight")
        self.inputs.new(NLSocketAlphaFloat.bl_idname, "IK Distance")
        self.inputs.new(NLSocketIKMode.bl_idname, "Distance Mode")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionEditArmatureConstraint"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "armature",
            "constraint_name",
            "enforced_factor",
            "primary_target",
            "secondary_target",
            "active",
            "ik_weight",
            "ik_distance",
            "distance_mode"
        ]


_nodes.append(NLActionEditArmatureConstraint)


class NLActionSetBonePos(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetBonePos"
    bl_label = "Set Bone Position"
    bl_icon = 'BONE_DATA'
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Bone Name")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Set Pos")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetBonePos"

    def get_input_sockets_field_names(self):
        return ["condition", "armature", "bone_name", "set_translation"]


_nodes.append(NLActionSetBonePos)


class NLActionEditBoneNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionEditBoneNode"
    bl_label = "Edit Armature Bone"
    bl_icon = 'BONE_DATA'
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Armature")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Bone Name")
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
        return "bgelogic.ActionEditBone"

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


class NLActionSetDynamicsNode(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetDynamicsNode"
    bl_label = "Set Dynamics (Physics)"
    bl_icon = 'FORCE_LENNARDJONES'
    nl_category = "Objects"
    nl_subcat = 'Data'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLBooleanSocket.bl_idname, "Suspend")
        self.inputs.new(NLBooleanSocket.bl_idname, "Ghost")
        self.inputs[-1].value = False
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetDynamics"

    def get_input_sockets_field_names(self):
        return ["condition", "game_object", "activate", 'ghost']


_nodes.append(NLActionSetDynamicsNode)


class NLActionSetMousePosition(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetMousePosition"
    bl_label = "Set Position"
    bl_icon = 'RESTRICT_SELECT_OFF'
    nl_category = "Input"
    nl_subcat = 'Mouse'

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
        return "bgelogic.ActionSetMousePosition"

    def get_input_sockets_field_names(self):
        return ["condition", "screen_x", "screen_y"]


_nodes.append(NLActionSetMousePosition)


class NLActionSetMouseCursorVisibility(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetMouseCursorVisibility"
    bl_label = "Cursor Visibility"
    bl_icon = 'VIS_SEL_10'
    nl_category = "Input"
    nl_subcat = 'Mouse'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLBooleanSocket.bl_idname, "Visible")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetMouseCursorVisibility"

    def get_input_sockets_field_names(self):
        return ["condition", "visibility_status"]


_nodes.append(NLActionSetMouseCursorVisibility)


class NLActionAddSoundDevice(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionAddSoundDevice"
    bl_label = "New Sound Device"
    bl_icon = 'MUTE_IPO_OFF'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'custom'
        self.inputs.new(NLSocketDistanceModels.bl_idname, "Distance Model")
        self.inputs[-1].value = 'INVERSE_CLAMPED'
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Volume")
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Doppler Factor")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Speed of Sound")
        self.inputs[-1].value = 343.3
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["DONE"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionAddSoundDevice"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "name",
            "distance_model",
            "volume",
            "doppler_fac",
            "sound_speed"
        ]


_nodes.append(NLActionAddSoundDevice)


class NLActionStart3DSound(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStart3DSound"
    bl_label = "3D Sound"
    bl_icon = 'MUTE_IPO_ON'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Speaker")
        self.inputs.new(NLFilePathSocket.bl_idname, "Sound File")
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Pitch")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Volume")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Maximum Distance")
        self.inputs[-1].value = 500.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

    def get_output_socket_varnames(self):
        return ["DONE", "HANDLE"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStart3DSound"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "speaker",
            "sound",
            "loop_count",
            "pitch",
            "volume",
            "distance_max"
        ]


_nodes.append(NLActionStart3DSound)


class NLActionStart3DSoundAdv(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStart3DSoundAdv"
    bl_label = "3D Sound (Advanced)"
    bl_icon = 'MUTE_IPO_ON'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Speaker")
        self.inputs.new(NLFilePathSocket.bl_idname, "Sound File")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Device")
        self.inputs[-1].value = 'default3D'
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Pitch")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Volume")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Attenuation")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Reference Distance")
        self.inputs[-1].value = 1.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Maximum Distance")
        self.inputs[-1].value = 1000.0
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Cone Inner Angle")
        self.inputs[-1].value = 360
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Cone Outer Angle")
        self.inputs[-1].value = 360
        self.inputs.new(NLPosFloatFormatSocket.bl_idname, "Cone Outer Volume")
        self.inputs[-1].value = 0.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

    def get_output_socket_varnames(self):
        return ["DONE", "HANDLE"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStart3DSoundAdv"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "speaker",
            "sound",
            "device",
            "loop_count",
            "pitch",
            "volume",
            "attenuation",
            "distance_ref",
            "distance_max",
            "cone_inner_angle",
            "cone_outer_angle",
            "cone_outer_volume"
        ]


_nodes.append(NLActionStart3DSoundAdv)


class NLActionStartSound(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStartSound"
    bl_label = "2D Sound"
    bl_icon = 'FILE_SOUND'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFilePathSocket.bl_idname, "Sound File")
        self.inputs.new(NLSocketLoopCount.bl_idname, "Mode")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Pitch")
        self.inputs.new(NLPositiveFloatSocket.bl_idname, "Volume")
        self.inputs[-1].value = 1.0
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')
        self.outputs.new(NLParameterSocket.bl_idname, 'Sound')

    def get_output_socket_varnames(self):
        return ["DONE", "HANDLE"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStartSound"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "sound",
            "loop_count",
            "pitch",
            "volume"
        ]


_nodes.append(NLActionStartSound)


class NLActionStopAllSounds(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStopAllSounds"
    bl_label = "Stop All Sounds"
    bl_icon = 'CANCEL'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStopAllSounds"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLActionStopAllSounds)


class NLActionStopSound(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStopSound"
    bl_label = "Stop Sound"
    bl_icon = 'SNAP_FACE'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Sound")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStopSound"

    def get_input_sockets_field_names(self):
        return ["condition", "sound"]


_nodes.append(NLActionStopSound)


class NLActionPauseSound(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionPauseSound"
    bl_label = "Pause Sound"
    bl_icon = 'PAUSE'
    nl_category = "Sound"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLParameterSocket.bl_idname, "Sound")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionPauseSound"

    def get_input_sockets_field_names(self):
        return ["condition", "sound"]


_nodes.append(NLActionPauseSound)


class NLActionEndGame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionEndGame"
    bl_label = "Quit Game"
    bl_icon = 'SCREEN_BACK'
    nl_category = "Game"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionEndGame"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLActionEndGame)


class NLActionRestartGame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRestartGame"
    bl_label = "Restart Game"
    bl_icon = 'LOOP_BACK'
    nl_category = "Game"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRestartGame"

    def get_input_sockets_field_names(self):
        return ["condition"]


_nodes.append(NLActionRestartGame)


class NLActionStartGame(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionStartGame"
    bl_label = "Start Game"
    nl_category = "Game"

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLFilePathSocket.bl_idname, "File name")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionStartGame"

    def get_input_sockets_field_names(self):
        return ["condition", "file_name"]


_nodes.append(NLActionStartGame)


class NLParameterGetGlobalValue(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterGetGlobalValue"
    bl_label = "Get Global Value"
    nl_category = "Values"
    nl_subcat = 'Global'

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'general'
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Key")
        self.inputs[-1].value = 'var_name'
        self.inputs.new(NLValueFieldSocket.bl_idname, "Default Value")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["data_id", "key", 'default']

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterGetGlobalValue"


_nodes.append(NLParameterGetGlobalValue)


class NLActionSetGlobalValue(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionSetGlobalValue"
    bl_label = "Set Global Value"
    nl_category = "Values"
    nl_subcat = 'Global'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLPseudoConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Name")
        self.inputs[-1].value = 'general'
        self.inputs.new(NLBooleanSocket.bl_idname, "Persistent")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Key")
        self.inputs[-1].value = 'var_name'
        self.inputs.new(NLValueFieldSocket.bl_idname, "")
        self.outputs.new(NLConditionSocket.bl_idname, 'Done')

    def get_output_socket_varnames(self):
        return ["OUT"]

    def get_input_sockets_field_names(self):
        return ["condition", "data_id", "persistent", "key", "value"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionSetGlobalValue"


_nodes.append(NLActionSetGlobalValue)


class NLParameterFormattedString(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterFormattedString"
    bl_label = "Formatted String"
    nl_category = "Values"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "Format String")
        self.inputs[-1].value = "Value A:{}, Value B:{}"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "A")
        self.inputs[-1].value = "Hello"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "B")
        self.inputs[-1].value = "World"
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "C")
        self.inputs.new(NLQuotedStringFieldSocket.bl_idname, "D")
        self.outputs.new(NLParameterSocket.bl_idname, "String")

    def get_input_sockets_field_names(self):
        return ["format_string", "value_a", "value_b", "value_c", "value_d"]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterFormattedString"


_nodes.append(NLParameterFormattedString)


class NLActionRandomInteger(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRandomInteger"
    bl_label = "Random Integer"
    nl_category = "Values"
    nl_subcat = 'Random'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Max")
        self.inputs.new(NLIntegerFieldSocket.bl_idname, "Min")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRandomInt"

    def get_output_socket_varnames(self):
        return ["OUT_A"]


_nodes.append(NLActionRandomInteger)


class NLActionRandomFloat(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRandomFloat"
    bl_label = "Random Float"
    nl_category = "Values"
    nl_subcat = 'Random'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Max")
        self.inputs.new(NLFloatFieldSocket.bl_idname, "Min")
        self.outputs.new(NLParameterSocket.bl_idname, "Value")

    def get_input_sockets_field_names(self):
        return ["max_value", "min_value"]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRandomFloat"

    def get_output_socket_varnames(self):
        return ["OUT_A"]


_nodes.append(NLActionRandomFloat)


class NLParameterDistance(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterDistance"
    bl_label = "Distance"
    nl_category = "Math"

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLVec3FieldSocket.bl_idname, "A")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "B")
        self.outputs.new(NLParameterSocket.bl_idname, "Distance")

    def get_input_sockets_field_names(self):
        return ["parama", "paramb"]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterDistance"


_nodes.append(NLParameterDistance)


class NLParameterKeyboardKeyCode(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterKeyboardKeyCode"
    bl_label = "Key Code"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    value: bpy.props.StringProperty(update=update_tree_code)

    def init(self, context):
        NLParameterNode.init(self, context)
        self.inputs.new(NLKeyboardKeySocket.bl_idname, "")
        self.outputs.new(NLParameterSocket.bl_idname, "Code")

    def get_input_sockets_field_names(self):
        return ["key_code"]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterKeyboardKeyCode"


_nodes.append(NLParameterKeyboardKeyCode)


class NLActionMoveTo(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionMoveTo"
    bl_label = "Move To"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

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
        return "bgelogic.ActionMoveTo"


_nodes.append(NLActionMoveTo)


class NLActionTranslate(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionTranslate"
    bl_label = "Translate"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

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
        return "bgelogic.ActionTranslate"


_nodes.append(NLActionTranslate)


class NLActionRotateTo(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionRotateTo"
    bl_label = "Rotate To"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Object")
        self.inputs.new(NLVec3FieldSocket.bl_idname, "Target")
        self.inputs.new(NLSocketLocalAxis.bl_idname, "Rot Axis")
        self.inputs.new(NLSocketOrientedLocalAxis.bl_idname, "Front")
        self.outputs.new(NLConditionSocket.bl_idname, "When Done")

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "moving_object",
            "target_point",
            "rot_axis",
            "front_axis"
        ]

    def get_netlogic_class_name(self):
        return "bgelogic.ActionRotateTo"


_nodes.append(NLActionRotateTo)


class NLActionNavigate(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionNavigate"
    bl_label = "Move To with Navmesh"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Moving Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Rotating Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Navmesh Object")
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
        self.outputs.new(NLConditionSocket.bl_idname, "When Reached")

    def get_netlogic_class_name(self):
        return "bgelogic.ActionNavigateWithNavmesh"

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
            "rot_speed"
        ]


_nodes.append(NLActionNavigate)


class NLActionFollowPath(bpy.types.Node, NLActionNode):
    bl_idname = "NLActionFollowPath"
    bl_label = "Follow Path"
    nl_category = "Objects"
    nl_subcat = 'Transformation'

    def init(self, context):
        NLActionNode.init(self, context)
        self.inputs.new(NLConditionSocket.bl_idname, "Condition")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Moving Object")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Rotating Object")
        self.inputs.new(
            NLGameObjectSocket.bl_idname,
            "Path (Parent of a set of Empties)"
        )
        self.inputs.new(NLBooleanSocket.bl_idname, "Loop")
        self.inputs.new(NLGameObjectSocket.bl_idname, "Optional Navmesh")
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
        return "bgelogic.ActionFollowPath"

    def get_input_sockets_field_names(self):
        return [
            "condition",
            "moving_object",
            "rotating_object",
            "path_parent",
            "loop",
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


_enum_predefined_math_fun = {
    ("User Defined", "User Defined", "A formula defined by the user"),
    ("exp(a)", "exp(e)", "e to the power a"),
    ("pow(a,b)", "pow(a,b)", "a to the power b"),
    ("log(a)", "log(a)", "natural log of a"),
    ("log10(a)", "log10(a)", "base 10 log of a"),
    ("acos(a)", "acos(a)", "arc cosine of a, radians"),
    ("asin(a)", "asin(a)", "arc sine of a, radians"),
    ("atan(a)", "atan(a)", "arc tangent of a, radians"),
    ("atan2(a,b)", "atan2(a,b)", "atan(a / b), radians"),
    ("cos(a)", "cos(a)", "cosine of a, radians"),
    ("hypot(a,b)", "hypot(a,b)", "sqrt(a*a + b*b)"),
    ("sin(a)", "sin(a)", "sine of a, radians"),
    ("tan(a)", "tan(a)", "tangent of a, radians"),
    ("degrees(a)", "degrees(a)", "convert a from radians to degrees"),
    ("radians(a)", "radians(a)", "convert a from degrees to radians"),
    ("acosh(a)", "acosh(a)", "inverse hyperbolic cosine of a"),
    ("asinh(a)", "asinh(a)", "inverse hyperbolic cosing of a"),
    ("atanh(a)", "atanh(a)", "inverse hyperbolic tangent of a"),
    ("cosh(a)", "cosh(a)", "hyperbolic cosine of a"),
    ("sinh(a)", "sinh(a)", "hyperbolic sine of a"),
    ("tanh(a)", "tanh(a)", "hyperbolic tangent of a"),
    ("pi", "pi", "the PI constant"),
    ("e", "e", "the e constant"),
    ("ceil(a)", "ceil(a)", "smallest integer value = or > to a"),
    ("sign(a)", "sign(a)", "0 if a is 0, -1 if a < 0, 1 if a > 0"),
    ("abs(a)", "abs(a)", "absolute value of a"),
    ("floor(a)", "floor(a)", "largest integer value < or = to a"),
    ("mod(a,b)", "mod(a,b)", "a modulo b"),
    ("sqrt(a)", "sqrt(a)", "square root of a"),
    ("curt(a)", "curt(a)", "cubic root of a"),
    ("str(a)", "str(a)", "a (non string value) converted to a string"),
    ("int(a)", "int(a)", "a (integer string) converted to an integer value"),
    ("float(a)", "float(a)", "a (float string) converted to a float value")
}


class NLParameterMathFun(bpy.types.Node, NLParameterNode):
    bl_idname = "NLParameterMathFun"
    bl_label = "Formula"
    nl_category = "Math"

    def on_fun_changed(self, context):
        if(self.predefined_formulas != "User Defined"):
            self.value = self.predefined_formulas
        update_tree_code(self, context)

    value: bpy.props.StringProperty(
        update=update_tree_code
    )
    predefined_formulas: bpy.props.EnumProperty(
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

    def get_nonsocket_fields(self):
        return [("formula", '"{0}"'.format(self.value))]

    def get_netlogic_class_name(self):
        return "bgelogic.ParameterMathFun"


_nodes.append(NLParameterMathFun)
