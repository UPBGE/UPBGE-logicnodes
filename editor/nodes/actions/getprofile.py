from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetProfile(LogicNodeActionType):
    bl_idname = "NLActionGetPerformanceProfileNode"
    bl_label = "Get Profile"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULGetPerformanceProfile"
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", None, {'show_prop': True})
        self.add_input(NodeSocketLogicBoolean, "Print Profile")
        self.add_input(NodeSocketLogicBoolean, "Evaluated Nodes")
        self.add_input(NodeSocketLogicBoolean, "Nodes per Second")
        self.add_input(NodeSocketLogicBoolean, "Nodes per Tick")
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicString, 'Profile')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "DATA"]

    def get_input_names(self):
        return [
            "condition",
            "print_profile",
            "check_evaluated_cells",
            'check_average_cells_per_sec',
            'check_cells_per_tick'
        ]
