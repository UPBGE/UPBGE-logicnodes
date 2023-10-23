from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython


@node_type
class LogicNodeResumeSound(LogicNodeActionType):
    bl_idname = "NLActionResumeSound"
    bl_label = "Resume Sound"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULResumeSound"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicPython, "Sound")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition", "sound"]
