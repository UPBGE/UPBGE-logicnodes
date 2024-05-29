from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeFModLoadBank(LogicNodeActionType):
    bl_idname = "LogicNodeFModLoadBank"
    bl_label = "FMod Load Bank"
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModLoadBankNode"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicString, "Path", 'path')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)
