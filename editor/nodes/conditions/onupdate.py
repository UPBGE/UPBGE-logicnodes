from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnUpdate(LogicNodeConditionType):
    bl_idname = "NLOnUpdateConditionNode"
    bl_label = "On Update"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULOnUpdate"
