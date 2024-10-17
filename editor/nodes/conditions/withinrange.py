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
    bl_description = 'Check if a value is within or outside of a range'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULWithinRange"

    operator: EnumProperty(
        name='Mode',
        items=_enum_in_or_out
    )

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicVectorXY, "Range", 'range', {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min", 'min_value')
        self.add_input(NodeSocketLogicFloat, "Max", 'max_value')
        self.add_output(NodeSocketLogicCondition, "If True", 'OUT')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", repr(self.operator))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["value", "range", "min_value", "max_value"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['OUT']
