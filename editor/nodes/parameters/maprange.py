from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeMapRange(LogicNodeParameterType):
    bl_idname = "NLMapRangeNode"
    bl_label = "Map Range"
    nl_category = "Math"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicFloat, "From Min")
        self.add_input(NodeSocketLogicFloat, "From Max", {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, "To Min")
        self.add_input(NodeSocketLogicFloat, "To Max", {'value': 1.0})
        self.add_output(NodeSocketLogicParameter, "Result")

    def get_netlogic_class_name(self):
        return "ULMapRange"

    def get_input_names(self):
        return ["value", "from_min", "from_max", "to_min", "to_max"]

    def get_output_names(self):
        return ["OUT"]
