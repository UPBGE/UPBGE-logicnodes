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
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value")
        self.add_output(NodeSocketLogicCondition, "If None")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    nl_class = "ULNone"

    def get_input_names(self):
        return ["checked_value"]
