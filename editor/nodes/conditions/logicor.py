from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicOr(LogicNodeConditionType):
    bl_idname = "NLConditionOrNode"
    bl_label = "Or"
    bl_width_min = 60
    bl_width_default = 80
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOr"

    deprecated = True
    deprecation_message = 'Replaced by "Gate" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'A')
        self.add_input(NodeSocketLogicCondition, 'B')
        self.add_output(NodeSocketLogicCondition, 'A or B')
        LogicNodeConditionType.init(self, context)
        self.hide = True

    def get_input_names(self):
        return ["ca", "cb"]
