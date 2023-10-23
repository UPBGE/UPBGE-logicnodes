from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicAndNot(LogicNodeConditionType):
    bl_idname = "NLConditionAndNotNode"
    bl_label = "And Not"
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Gate" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "A")
        self.add_input(NodeSocketLogicCondition, "B")
        self.add_output(NodeSocketLogicCondition, "If A and not B")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    nl_class = "ULAndNot"

    def get_input_names(self):
        return ["condition_a", "condition_b"]
