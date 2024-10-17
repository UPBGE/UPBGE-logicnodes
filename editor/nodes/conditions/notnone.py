from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicParameter
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeNotNone(LogicNodeConditionType):
    bl_idname = "NLConditionNotNoneNode"
    bl_label = "Not None"
    bl_description = 'Check if a value evaluates to anything but "None"'
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULNotNone"

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value", 'checked_value')
        self.add_output(NodeSocketLogicCondition, "If Not None", 'OUT')
        LogicNodeConditionType.init(self, context)
        self.hide = True

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["checked_value"]
