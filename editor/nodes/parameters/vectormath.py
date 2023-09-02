from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_vector_math_options
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeVectorMath(LogicNodeParameterType):
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
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2")
        self.add_input(NodeSocketLogicFloatFactor, "Factor")
        self.inputs[-1].value = 1.0
        self.add_input(NodeSocketLogicFloat, "Scale")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 3")
        self.add_input(NodeSocketLogicFloat, "IOR")
        self.add_output(NodeSocketLogicParameter, 'Result')
        self.update_draw()

    def get_netlogic_class_name(self):
        return "ULVectorMath"

    def update_draw(self):
        if len(self.inputs) < 6:
            return
        vtype = self.operator
        v2 = self.inputs[1]
        fac = self.inputs[2]
        sca = self.inputs[3]
        v3 = self.inputs[4]
        ior = self.inputs[5]

        v2.enabled = vtype in ['dot', 'cross', 'project', 'distance', 'faceforward', 'divide', 'multiply', 'subtract', 'add', 'lerp', 'slerp', 'multadd', 'angle', 'angle_signed']
        fac.enabled = vtype in ['lerp', 'slerp']
        sca.enabled = vtype in ['scale']
        v3.enabled = vtype in ['faceforward', 'multadd', 'slerp', 'angle_signed']
        ior.enabled = vtype in ['refract']

    def get_input_names(self):
        return ["vector", 'vector_2', 'factor', 'scale', 'vector_3', 'ior']

    def get_output_names(self):
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
