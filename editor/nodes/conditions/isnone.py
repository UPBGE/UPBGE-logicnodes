from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicParameter
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeIsNone(LogicNodeConditionType):
    bl_idname = "NLConditionNone"
    bl_label = "Is None"
    bl_width_min = 60
    bl_width_default = 80
    bl_description = 'Check if a value evaluates to "None"'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULNone"

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value", 'checked_value')
        self.add_output(NodeSocketLogicCondition, "If None", 'OUT')
        LogicNodeConditionType.init(self, context)
        self.hide = True

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["checked_value"]
