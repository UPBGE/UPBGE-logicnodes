from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean
from ...enum_types import _enum_greater_less
from bpy.props import EnumProperty


@node_type
class LogicNodeThreshold(LogicNodeParameterType):
    bl_idname = "NLThresholdNode"
    bl_label = "Threshold"
    nl_module = 'parameters'

    operator: EnumProperty(
        name='Operation',
        items=_enum_greater_less
    )

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "Else 0", {'value': True})
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicFloat, "Threshold")
        self.add_output(NodeSocketLogicParameter, "Value")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", f'"{self.operator}"')]

    nl_class = "ULThreshold"

    def get_input_names(self):
        return ['else_z', "value", "threshold"]

    def get_output_names(self):
        return ["OUT"]
