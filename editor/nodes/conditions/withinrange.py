from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXY
from ...enum_types import _enum_in_or_out
from bpy.props import EnumProperty


@node_type
class LogicNodeWithinRange(LogicNodeConditionType):
    bl_idname = "NLWithinRangeNode"
    bl_label = "Within Range"
    nl_module = 'uplogic.nodes.parameters'

    operator: EnumProperty(
        name='Mode',
        items=_enum_in_or_out
    )

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicVectorXY, "Range", {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min")
        self.add_input(NodeSocketLogicFloat, "Max")
        self.add_output(NodeSocketLogicCondition, "If True")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", f'"{self.operator}"')]

    nl_class = "ULWithinRange"

    def get_input_names(self):
        return ["value", "range", "min_value", "max_value"]

    def get_output_names(self):
        return ['OUT']
