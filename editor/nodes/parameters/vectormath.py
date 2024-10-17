from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter
from bpy.props import EnumProperty


_operations = [
    ('', 'Functions', ''),
    ('0', 'Add', 'A + B'),
    ('1', 'Subtract', 'A - B'),
    ('2', 'Multiply', 'Entry-wise multiply'),
    ('3', 'Divide', 'Entry-wise divide'),
    ('4', 'Multiply Add', 'A * B + C'),
    ('5', 'Matrix Multiply', 'Transform A by B'),
    ('6', 'Angle', 'Angle between A and B'),
    ('7', 'Signed Angle', 'Signed angle between A and B, measured around Up axis'),
    None,
    ('8', 'Cross Product', 'A cross B'),
    ('9', 'Project', 'Project A onto B'),
    ('10', 'Reflect', "Reflect A around the normal B. B doesn't need to be normalized"),
    ('11', 'Refract', 'For a given incident vector A, surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R'),
    ('12', 'Faceforward', 'Orients a vector A to point away from a surface B as defined by its normal C.'),
    ('13', 'Dot Product', 'A dot B'),
    ('', '', ''),
    ('14', 'Mix (Lerp)', 'Linear Interpolation from A to B'),
    ('15', 'Spherical Lerp', 'Spherical Linear Interpolation from A to B'),
    None,
    ('16', 'Distance', 'Distance between A and B'),
    ('17', 'Length', 'Length of A'),
    ('18', 'Scale', 'A multiplied by Scale'),
    None,
    ('19', 'Normalize', 'Normalize A'),
    ('20', 'Absolute', 'Entry-wise absolute'),
    ('21', 'Negate', 'Entry-wise inversion'),
    ('', 'Comparison', ''),
    ('22', 'Minimum', 'Entry-wise minimum'),
    ('23', 'Maximum', 'Entry-wise maximum'),
    ('', 'Rounding', ''),
    ('24', 'Round', 'Entry-wise round'),
    ('25', 'Floor', 'Entry-wise floor'),
    ('26', 'Ceil', 'Entry-wise ceil'),
    ('27', 'Fraction', 'The fraction part of A entry-wise'),
    ('28', 'Modulo', 'Entry-wise modulo (A % B)'),
    ('29', 'Wrap', 'Entry-wise wrap(A,B)'),
    ('30', 'Snap', 'Round A to the largest integer multiple of B less than or equal A'),
    ('', 'Trigonometric', ''),
    ('31', 'Sine', 'Entry-wise sin(A)'),
    ('32', 'Cosine', 'Entry-wise cos(A)'),
    ('33', 'Tangent', 'Entry-wise tan(A)')
]


@node_type
class LogicNodeVectorMath(LogicNodeParameterType):
    bl_idname = "LogicNodeVectorMath"
    bl_label = "Vector Math"
    bl_description = 'Perform mathematical operations with vectors'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "VectorMathNode"

    def update_draw(self, context=None):
        mode = int(self.operator)
        ipts = self.inputs
        a = ipts[0]
        b = ipts[1]
        c = ipts[2]
        v = ipts[3]
        vf = ipts[4]

        opts = self.outputs
        _float = opts[0]
        _vec = opts[1]

        a.name = 'Vector'
        b.name = 'Vector'
        c.name = 'Vector'
        v.name = 'Value'

        self.set_socket_state(_vec, True, 'Result')
        self.set_socket_state(_float, False, 'Result')

        b.enabled = mode not in [
            17, 18, 19, 20, 21, 24, 25, 26, 27, 31, 32, 33
        ]
        c.enabled = mode in [
            4, 7, 12, 29
        ]
        
        _float.enabled = mode in [
            6, 7, 13, 16, 17
        ]
        _vec.enabled = not _float.enabled
        
        v.enabled = mode in [11, 18]
        vf.enabled = mode in [14, 15]
        
        match mode:
            case 4:
                self.set_socket_state(b, True, 'Multiplier')
                self.set_socket_state(c, True, 'Addend')
            case 7:
                self.set_socket_state(c, True, 'Up')
            case 11:
                self.set_socket_state(v, True, 'IOR')
            case 12:
                self.set_socket_state(b, True, 'Incident')
                self.set_socket_state(c, True, 'Reference')
            case 18:
                self.set_socket_state(v, True, 'Scale')
            case 29:
                self.set_socket_state(b, True, 'Max')
                self.set_socket_state(c, True, 'Min')
            case 30:
                self.set_socket_state(b, True, 'Increment')
        # self.nl_label = _operations[mode][1]

    operator: EnumProperty(
        name='Operation',
        default='0',
        items=_operations,
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1", 'vector_a')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2", 'vector_b')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 3", 'vector_c')
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'value', {'default_value': 0.5})
        self.add_output(NodeSocketLogicParameter, 'Result', 'RESULT')
        self.add_output(NodeSocketLogicVectorXYZ, 'Result', 'RESULT_VECTOR')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operator', text='')

    def get_attributes(self):
        return [("operator", int(self.operator))]
