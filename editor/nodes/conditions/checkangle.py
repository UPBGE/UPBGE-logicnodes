from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_logic_operators
from bpy.props import EnumProperty


@node_type
class LogicNodeCheckAngle(LogicNodeConditionType):
    bl_idname = "NLVectorAngleCheck"
    bl_label = "Check Angle"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULVectorAngleCheck"
    deprecated = True
    deprecation_message = 'This node will be removed in a future update; use Vector Math and Compare instead'

    operator: EnumProperty(name='Operation', items=_enum_logic_operators)

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1", 'vector')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2", 'vector_2')
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_output(NodeSocketLogicCondition, 'Result', 'OUT')
        self.add_output(NodeSocketLogicFloat, "Angle", 'ANGLE')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operator', text='')

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["vector", 'vector_2', 'value']

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['OUT', 'ANGLE']

    def get_attributes(self):
        return [("op", repr(self.operator))]
