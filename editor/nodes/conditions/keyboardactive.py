from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeKeyboardActive(LogicNodeConditionType):
    bl_idname = "NLKeyboardActive"
    bl_label = "Keyboard Active"
    bl_description = 'Register keyboard activity'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULKeyboardActive"

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, 'Active', 'OUT')
        LogicNodeConditionType.init(self, context)
