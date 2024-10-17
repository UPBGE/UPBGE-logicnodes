from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_in_or_out
from bpy.props import EnumProperty


@node_type
class LogicNodeRangedThreshold(LogicNodeParameterType):
    bl_idname = "NLRangedThresholdNode"
    bl_label = "Ranged Threshold"
    bl_description = 'Get a value inside or outside of a range, else 0'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULRangedThreshold"

    operator: EnumProperty(
        items=_enum_in_or_out,
        name='Mode'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicVectorXY, "Threshold", 'threshold', {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min", 'min_value')
        self.add_input(NodeSocketLogicFloat, "Max", 'max_value')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", repr(self.operator))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["value", "threshold", "min_value", "max_value"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['OUT']
