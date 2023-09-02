from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_in_or_out
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeRangedThreshold(LogicNodeParameterType):
    bl_idname = "NLRangedThresholdNode"
    bl_label = "Ranged Threshold"
    nl_category = "Math"
    nl_module = 'parameters'

    operator: EnumProperty(
        items=_enum_in_or_out,
        update=update_draw
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicVectorXY, "Threshold", {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min")
        self.add_input(NodeSocketLogicFloat, "Max")
        self.add_output(NodeSocketLogicParameter, "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("operator", lambda: f'"{self.operator}"')
        ]

    def get_netlogic_class_name(self):
        return "ULRangedThreshold"

    def get_input_names(self):
        return ["value", "threshold", "min_value", "max_value"]

    def get_output_names(self):
        return ['OUT']
