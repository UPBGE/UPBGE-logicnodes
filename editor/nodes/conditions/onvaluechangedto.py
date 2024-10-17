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
    bl_description = 'Check if a value has changed to something specific from another'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULValueChangedTo"

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value", 'monitored_value')
        self.add_input(NodeSocketLogicValue, "", 'trigger_value', {'value_type': 'BOOLEAN', 'default_value': 'True'})
        self.add_output(NodeSocketLogicCondition, "Result", 'OUT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["monitored_value", "trigger_value"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
