from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeShowProfile(LogicNodeActionType):
    bl_idname = "NLSetProfile"
    bl_label = "Show Profile"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetProfile"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicBoolean, 'Show')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "use_profile"]
