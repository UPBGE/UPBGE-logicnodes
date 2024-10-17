from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive


@node_type
class LogicNodeSetTimescale(LogicNodeActionType):
    bl_idname = "NLActionSetTimeScale"
    bl_label = "Set Timescale"
    bl_description = 'Set the timescale of the scene'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetTimeScale"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicFloatPositive, "Timescale", 'timescale')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "timescale"]
