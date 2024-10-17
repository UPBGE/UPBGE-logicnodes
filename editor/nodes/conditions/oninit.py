from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnInit(LogicNodeConditionType):
    bl_idname = "NLOnInitConditionNode"
    bl_label = "On Init"
    bl_description = 'On first frame'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOnInit"

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "Out", 'OUT')
        LogicNodeConditionType.init(self, context)
        self.hide = True
