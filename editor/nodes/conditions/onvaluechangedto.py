from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicValue
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeOnValueChangedTo(LogicNodeConditionType):
    """True if input is equal to given value after changing"""
    bl_idname = "NLConditionValueTriggerNode"
    bl_label = "On Value Changed To"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value")
        self.add_input(NodeSocketLogicValue, "", None, {'value_type': 'BOOLEAN', 'default_value': 'True'})
        self.add_output(NodeSocketLogicCondition, "Result")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULValueChangedTo"

    def get_input_names(self):
        return ["monitored_value", "trigger_value"]

    def get_output_names(self):
        return ['OUT']
