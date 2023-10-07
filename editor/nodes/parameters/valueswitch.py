from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeValueSwitch(LogicNodeParameterType):
    bl_idname = "NLValueSwitch"
    bl_label = "Value Switch"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "A if True, else B")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicParameter, "Result")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULValueSwitch"

    def get_input_names(self):
        return ["condition", 'val_a', 'val_b']

    def get_output_names(self):
        return ['VAL']
