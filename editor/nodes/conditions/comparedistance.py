from ...enum_types import _enum_logic_operators
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatPositive
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeCompareDistance(LogicNodeConditionType):
    bl_idname = "NLConditionDistanceCheck"
    bl_label = "Compare Distance"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULCheckDistance"

    operation: EnumProperty(items=_enum_logic_operators)
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "A")
        self.add_input(NodeSocketLogicVectorXYZ, "B")
        self.add_input(NodeSocketLogicFloatPositive, "Value")
        self.add_input(NodeSocketLogicFloat, "Hyst", None, {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Out")
        self.add_output(NodeSocketLogicFloat, "Distance")
        LogicNodeConditionType.init(self, context)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, 'operation', text='')

    def get_output_names(self):
        return ['OUT', 'DIST']

    def get_input_names(self):
        return ["param_a", "param_b", "dist", '_old_hyst']

    def get_attributes(self):
        return [("operation", self.operation)]
