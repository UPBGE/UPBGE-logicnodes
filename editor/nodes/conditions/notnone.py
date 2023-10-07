from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicParameter
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeNotNone(LogicNodeConditionType):
    bl_idname = "NLConditionNotNoneNode"
    bl_label = "Not None"
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value")
        self.add_output(NodeSocketLogicCondition, "If Not None")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    nl_class = "ULNotNone"

    def get_input_names(self):
        return ["checked_value"]
