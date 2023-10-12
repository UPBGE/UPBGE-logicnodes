from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeLoadFileContent(LogicNodeActionType):
    bl_idname = "NLLoadFileContent"
    bl_label = "Load File Content"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULLoadFileContent"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_output(NodeSocketLogicCondition, 'Loaded')
        self.add_output(NodeSocketLogicCondition, 'Updated')
        self.add_output(NodeSocketLogicFloatFactor, 'Status')
        self.add_output(NodeSocketLogicString, 'Datatype')
        self.add_output(NodeSocketLogicString, 'Item')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition']

    def get_output_names(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']
