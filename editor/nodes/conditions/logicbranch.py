from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeLogicBranch(LogicNodeConditionType):
    bl_idname = "NLParameterSwitchValue"
    bl_label = "Branch"
    bl_description = 'Branch a condition into its "True" and "False" states'
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULTrueFalse"

    search_tags = [
        ['Logic Branch', {}],
        ['True / False', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'state')
        self.add_output(NodeSocketLogicCondition, "True", 'TRUE')
        self.add_output(NodeSocketLogicCondition, "False", 'FALSE')
        LogicNodeConditionType.init(self, context)
        self.hide = True

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["state"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["TRUE", "FALSE"]
