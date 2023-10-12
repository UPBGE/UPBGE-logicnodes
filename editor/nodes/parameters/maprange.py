from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeMapRange(LogicNodeParameterType):
    bl_idname = "NLMapRangeNode"
    bl_label = "Map Range"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicFloat, "From Min")
        self.add_input(NodeSocketLogicFloat, "From Max", {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, "To Min")
        self.add_input(NodeSocketLogicFloat, "To Max", {'value': 1.0})
        self.add_output(NodeSocketLogicParameter, "Result")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULMapRange"

    def get_input_names(self):
        return ["value", "from_min", "from_max", "to_min", "to_max"]

    def get_output_names(self):
        return ["OUT"]
