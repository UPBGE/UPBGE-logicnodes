from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_vector_math_options
from ....utilities import WARNING_MESSAGES
from bpy.props import EnumProperty


@node_type
class LogicNodeVectorMathOld(LogicNodeParameterType):
    bl_idname = "NLVectorMath"
    bl_label = "Vector Math"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorMath"

    deprecated = True
    deprecation_message = 'Node still works but was updated, please replace.'

    def update_draw(self, context=None):
        if not self.ready:
            return
        vtype = self.operator
        v2 = self.inputs[1]
        fac = self.inputs[2]
        sca = self.inputs[3]
        v3 = self.inputs[4]
        ior = self.inputs[5]

        v2.enabled = vtype in ['dot', 'cross', 'project', 'distance', 'faceforward', 'divide', 'multiply', 'subtract', 'reflect', 'add', 'lerp', 'slerp', 'multadd', 'angle', 'angle_signed', 'matmul']
        fac.enabled = vtype in ['lerp', 'slerp']
        sca.enabled = vtype in ['scale']
        v3.enabled = vtype in ['faceforward', 'multadd', 'slerp', 'angle_signed']
        ior.enabled = vtype in ['refract']

        if len(self.outputs) > 1:
            fres = self.outputs[0]
            vres = self.outputs[1]
            fres.enabled = vtype in ['length', 'distance', 'angle', 'dot']
            vres.enabled = not fres.enabled

    operator: EnumProperty(
        name='Operation',
        items=_enum_vector_math_options,
        update=update_draw,
        default='add'
    )

    def check(self, tree):
        super().check(tree)
        if len(self.outputs) < 2:
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(f"Node '{self.name}' in tree '{tree.name}' changed outputs. Re-Add to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1", 'vector')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2", 'vector_2')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'factor', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Scale", 'scale')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 3", 'vector_3')
        self.add_input(NodeSocketLogicFloat, "IOR", 'ior')
        self.add_output(NodeSocketLogicParameter, 'Result', 'OUT')
        self.add_output(NodeSocketLogicVectorXYZ, 'Result', 'VOUT')
        LogicNodeParameterType.init(self, context)

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["vector", 'vector_2', 'factor', 'scale', 'vector_3', 'ior']

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'VOUT']

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operator', text='')

    def get_attributes(self):
        return [("op", repr(self.operator))]
