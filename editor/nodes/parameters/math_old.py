from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_math_operations
from bpy.props import EnumProperty


@node_type
class LogicNodeMathOld(LogicNodeParameterType):
    bl_idname = "NLArithmeticOpParameterNode"
    bl_label = "Math"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULMath"
    
    deprecated = True
    deprecation_message = 'Node still works but was updated, please replace.'

    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations
    )

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "A")
        self.add_input(NodeSocketLogicFloat, "B")
        self.add_output(NodeSocketLogicParameter, "Result")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_input_names(self):
        return ['collection']

    def get_attributes(self):
        return [("operator", f'OPERATORS.get("{self.operator}")')]

    def get_input_names(self):
        return ["operand_a", "operand_b"]

    def get_output_names(self):
        return ["OUT"]
