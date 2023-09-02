from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_math_operations
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeMath(LogicNodeParameterType):
    bl_idname = "NLArithmeticOpParameterNode"
    bl_label = "Math"
    nl_category = "Math"
    nl_module = 'parameters'
    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations,
        update=update_draw
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "A")
        self.add_input(NodeSocketLogicFloat, "B")
        self.add_output(NodeSocketLogicParameter, "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_input_names(self):
        return ['collection']

    def get_attributes(self):
        return [
            ("operator", f'OPERATORS.get("{self.operator}")')
        ]

    def get_netlogic_class_name(self):
        return "ULMath"

    def get_input_names(self):
        return ["operand_a", "operand_b"]

    def get_output_names(self):
        return ["OUT"]
