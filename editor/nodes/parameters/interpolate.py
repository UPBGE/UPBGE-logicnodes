from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeInterpolate(LogicNodeParameterType):
    bl_idname = "NLInterpolateValueNode"
    bl_label = "Interpolate"
    bl_description = 'Linear interpolation'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULInterpolate"

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "From", 'a')
        self.add_input(NodeSocketLogicFloat, "To", 'b')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'fac')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["a", "b", "fac"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
