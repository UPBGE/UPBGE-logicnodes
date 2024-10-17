from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeValueInvert(LogicNodeParameterType):
    bl_idname = "NLInvertValueNode"
    bl_label = "Invert"
    bl_description = 'Multiply a value by -1'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULInvertValue"

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_output(NodeSocketLogicFloat, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["value"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
