from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeInterpolate(LogicNodeParameterType):
    bl_idname = "NLInterpolateValueNode"
    bl_label = "Interpolate"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "From")
        self.add_input(NodeSocketLogicFloat, "To")
        self.add_input(NodeSocketLogicFloatFactor, "Factor")
        self.add_output(NodeSocketLogicParameter, "Value")

    def get_netlogic_class_name(self):
        return "ULInterpolate"

    def get_input_names(self):
        return ["a", "b", "fac"]

    def get_output_names(self):
        return ["OUT"]
