from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeOnNextFrame(LogicNodeConditionType):
    bl_idname = "NLConditionNextFrameNode"
    bl_label = "On Next Frame"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicBoolCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULOnNextTick"

    def get_input_names(self):
        return ["input_condition"]
