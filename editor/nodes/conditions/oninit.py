from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnInit(LogicNodeConditionType):
    bl_idname = "NLOnInitConditionNode"
    bl_label = "On Init"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULOnInit"
