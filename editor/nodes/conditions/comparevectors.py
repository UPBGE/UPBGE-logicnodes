from ...enum_types import _enum_logic_operators
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicXYZ
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicVectorXYZ
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeCompareVectors(LogicNodeConditionType):
    bl_idname = "NLConditionCompareVecs"
    bl_label = "Compare Vectors"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'conditions'
    deprecated = True

    operator: EnumProperty(name='Operator', items=_enum_logic_operators)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        self.add_input(NodeSocketLogicXYZ, "")
        self.add_input(NodeSocketLogicFloatPositive, "Threshold")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector A")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector B")
        self.add_output(NodeSocketLogicCondition, "If True")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULCompareVectors"

    def get_input_names(self):
        return ['all', 'threshold', "param_a", "param_b"]

    def get_output_names(self):
        return ['OUT']

    def get_attributes(self):
        return [("operator", f'{self.operator}')]
