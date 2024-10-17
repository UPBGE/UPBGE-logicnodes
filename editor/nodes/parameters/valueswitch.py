from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeValueSwitch(LogicNodeParameterType):
    bl_idname = "NLValueSwitch"
    bl_label = "Value Switch"
    bl_description = 'Choose between 2 values depending on an input value'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULValueSwitch"

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "A if True, else B", 'condition')
        self.add_input(NodeSocketLogicValue, "", 'val_a')
        self.add_input(NodeSocketLogicValue, "", 'val_b')
        self.add_output(NodeSocketLogicParameter, "Result", 'VAL')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'val_a', 'val_b']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['VAL']
