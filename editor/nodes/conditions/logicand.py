from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicAnd(LogicNodeConditionType):
    bl_idname = "NLConditionAndNode"
    bl_label = "And"
    bl_width_min = 60
    bl_width_default = 80
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Gate" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "A")
        self.add_input(NodeSocketLogicCondition, "B")
        self.add_output(NodeSocketLogicCondition, "If A and B")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    nl_class = "ULAnd"

    def get_input_names(self):
        return ["ca", "cb"]
