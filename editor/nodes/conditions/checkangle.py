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

    operator: EnumProperty(name='Operation', items=_enum_logic_operators)

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2")
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_output(NodeSocketLogicCondition, 'If True')
        self.add_output(NodeSocketLogicFloat, "Angle")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULVectorAngleCheck"

    def get_input_names(self):
        return ["vector", 'vector_2', 'value']

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            'operator',
            text=''
        )

    def get_output_names(self):
        return ['OUT', 'ANGLE']

    def get_attributes(self):
        return [("op", f'"{self.operator}"')]
