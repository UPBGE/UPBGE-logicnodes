from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnUpdate(LogicNodeConditionType):
    bl_idname = "NLOnUpdateConditionNode"
    bl_label = "On Update"
    bl_description = 'Every frame'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOnUpdate"

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "Out", 'OUT')
        LogicNodeConditionType.init(self, context)
        self.hide = True
