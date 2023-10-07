from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeLogicBranch(LogicNodeConditionType):
    bl_idname = "NLParameterSwitchValue"
    bl_label = "Branch"
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'conditions'

    search_tags = [
        ['Logic Branch', {}],
        ['True / False', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, "True")
        self.add_output(NodeSocketLogicCondition, "False")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    nl_class = "ULTrueFalse"

    def get_input_names(self):
        return ["state"]

    def get_output_names(self):
        return ["TRUE", "FALSE"]
