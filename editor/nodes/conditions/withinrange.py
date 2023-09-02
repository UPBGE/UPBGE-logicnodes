from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXY
from ...enum_types import _enum_in_or_out
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeWithinRange(LogicNodeConditionType):
    bl_idname = "NLWithinRangeNode"
    bl_label = "Within Range"
    nl_category = "Math"
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Mode',
        items=_enum_in_or_out,
        update=update_draw
    )

    def init(self, context):
        LogicNodeConditionType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicVectorXY, "Range", {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min")
        self.add_input(NodeSocketLogicFloat, "Max")
        self.add_output(NodeSocketLogicCondition, "If True")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", f'"{self.operator}"')]

    def get_netlogic_class_name(self):
        return "ULWithinRange"

    def get_input_names(self):
        return ["value", "range", "min_value", "max_value"]

    def get_output_names(self):
        return ['OUT']
