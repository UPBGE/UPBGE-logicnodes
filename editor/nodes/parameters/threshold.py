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
    bl_description = "Return a value only if it's greater or less than a threshold"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULThreshold"

    operator: EnumProperty(
        name='Operation',
        items=_enum_greater_less
    )

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "Else 0", 'else_z', {'default_value': True})
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicFloat, "Threshold", 'threshold')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [("operator", repr(self.operator))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ['else_z', "value", "threshold"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
