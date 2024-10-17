from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicParameter
from bpy.props import EnumProperty
from bpy.props import BoolProperty


_enum_operations = [
    ('', "Functions", ''),
    ("0", "Add", "A + B"),
    ("1", "Subtract", "A - B"),
    ("2", "Multiply", "A * B"),
    ("3", "Divide", "A / B"),
    ("4", "Multiply Add", "A * B + C"),
    ("5", "Modulo", "Remainder of A / B"),
    ("6", "Floor Divide", "Floored A / B"),
    None,
    ("7", "Power", "A power B"),
    ("8", "Logarithm", "Logarithm A base B"),
    ("9", "Square Root", "Square root of A"),
    ("10", "Inverse Square Root", "1 / Square root of A"),
    ("11", "Absolute", "Magnitude of A"),
    ("12", "Exponent", "exp(A)"),
    ("43", "Interpolate", "Interpolation from A to B"),
    ("", "Comparison", ''),
    ("13", "Minimum", "The minimum from A and B"),
    ("14", "Maximum", "The maximum from A and B"),
    ("15", "Less Than", "True if A < B else False"),
    ("16", "Greater Than", "True if A > B else False"),
    ("17", "Sign", "Returns the sign of A"),
    ("18", "Compare", "True if (A == B) within tolerance C else False"),
    ("19", "Smooth Minimum", "The minimum from A and B with smoothing C"),
    ("20", "Smooth Maximum", "The maximum from A and B with smoothing C"),
    ("", "Rounding", ''),
    ("21", "Round", "Round A to the nearest integer. Round upward if the fraction part is 0.5"),
    ("22", "Floor", "The largest integer smaller than or equal A"),
    ("23", "Ceil", "The smallest integer greater than or equal A"),
    ("24", "Truncate", "The integer part of A, removing fractional digits"),
    None,
    ("25" , "Fraction", "The fraction part of A"),
    ("26", "Truncated Modulo", "The remainder of truncated division using fmod(A,B)"),
    ("27", "Floored Modulo", "The remainder of floored division"),
    ("28", "Wrap", "Wrap value to range, wrap(A,B)"),
    ("29", "Snap", "Snap to increment, snap(A,B)"),
    ("30", "Ping-Pong", "Wraps a value and reverses every other cycle (A,B)"),
    ("", "Trigonometric", ''),
    ("31", "Sine", "sin(A)"),
    ("32", "Cosine", "cos(A)"),
    ("33", "Tangent", "tan(A)"),
    None,
    ("34", "Arcsine", "arcsin(A)"),
    ("35", "Arccosine", "arccos(A)"),
    ("36", "Arctangent", "arctan(A)"),
    ("37", "Arctan2", "The signed angle arctan(A / B)"),
    None,
    ("38", "Hyperbolic Sine", "sinh(A)"),
    ("39", "Hyperbolic Cosine", "cosh(A)"),
    ("40", "Hyperbolic Tangent", "tanh(A)"),
    ("", "Conversion", ''),
    ("41", "To Radians", "Convert from degrees to radians"),
    ("42", "To Degrees", "Convert from radians to degrees")
]

names = [
    "Add",
    "Subtract",
    "Multiply",
    "Divide",
    "Multiply Add",
    "Modulo",
    "Floor Divide",
    "Power",
    "Logarithm",
    "Square Root",
    "Inverse Square",
    "Absolute",
    "Exponent",
    "Minimum",
    "Maximum",
    "Less Than",
    "Greater Than",
    "Sign",
    "Compare",
    "Smooth Minimum",
    "Smooth Maximum",
    "Round",
    "Floor",
    "Ceil",
    "Truncate",
    "Fraction",
    "Truncated Modulo",
    "Floored Modulo",
    "Wrap",
    "Snap",
    "Ping-Pong"
    "Sine",
    "Cosine",
    "Tangent",
    "Arcsine",
    "Arccosine",
    "Arctangent",
    "Arctan2",
    "Hyperbolic Sine",
    "Hyperbolic Cosine",
    "Hyperbolic Tangent",
    "To Radians",
    "To Degrees",
    "Interpolate"
]


@node_type
class LogicNodeMath(LogicNodeParameterType):
    bl_idname = "LogicNodeMath"
    bl_label = "Math"
    bl_description = 'Perform a mathematical operation'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "MathNode"

    def update_draw(self, context=None):
        mode = int(self.operator)
        ipts = self.inputs
        a = ipts[0]
        b = ipts[1]
        c = ipts[2]
        d = ipts[3]
        
        opts = self.outputs
        _param = opts[0]
        _bool = opts[1]

        a.name = 'Value'
        b.name = 'Value'
        c.name = 'Value'
        self.set_socket_state(_param, True, 'Result')
        self.set_socket_state(_bool, False, 'Result')

        b.enabled = mode not in [
            9,
            10,
            11,
            12,
            17,
            21,
            22,
            23,
            24,
            25,
            31,
            32,
            33,
            34,
            35,
            36,
            38,
            39,
            40,
            41,
            42
        ]
        c.enabled = mode in [
            4,
            18,
            19,
            20,
            28
        ]
        d.enabled = mode == 43
        match mode:
            case 4:  # Multiply Add
                self.set_socket_state(b, True, 'Multiplier')
                self.set_socket_state(c, True, 'Addend')
            case 7:  # Power
                self.set_socket_state(a, True, 'Base')
                self.set_socket_state(b, True, 'Exponent')
            case 8:  # Logarithm
                self.set_socket_state(b, True, 'Base')
            case 15 | 16:  # < | >
                self.set_socket_state(b, True, 'Threshold')
                self.set_socket_state(_param, False)
                self.set_socket_state(_bool, True)
            case 18:  # Compare
                self.set_socket_state(c, True, 'Epsilon')
                self.set_socket_state(_param, False)
                self.set_socket_state(_bool, True)
            case 19 | 20:  # Smooth Min/Max
                self.set_socket_state(c, True, 'Distance')
            case 28:  # Wrap
                self.set_socket_state(b, True, 'Max')
                self.set_socket_state(c, True, 'Min')
            case 29:  # Snap
                self.set_socket_state(b, True, 'Increment')
            case 30:  # Ping Pong
                self.set_socket_state(b, True, 'Scale')
            case 41:  # Radians
                self.set_socket_state(a, True, 'Degrees')
            case 42:  # Degrees
                self.set_socket_state(a, True, 'Radians')
            case _:  # Default
                pass
        self.nl_label = names[mode]

    operator: EnumProperty(
        name='Operation',
        items=_enum_operations,
        default='0',
        update=update_draw
    )
    
    clamp: BoolProperty(name='Clamp', description='Clamp the resulting value from 0 to 1')

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "A", 'value_a')
        self.add_input(NodeSocketLogicFloat, "B", 'value_b')
        self.add_input(NodeSocketLogicFloat, "C", 'value_c')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'value_c')
        self.add_output(NodeSocketLogicParameter, "Result", 'RESULT')
        self.add_output(NodeSocketLogicBoolean, "Result", 'RESULT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")
        if int(self.operator) not in [15, 16, 18]:
            layout.prop(self, "clamp")

    def get_attributes(self):
        return [
            ("operator", f'MATH_OPERATORS[{int(self.operator)}]'),
            ("clamp", self.clamp if int(self.operator) not in [15, 16, 18] else False),
        ]
