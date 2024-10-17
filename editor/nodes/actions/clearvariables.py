from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFilePath


@node_type
class LogicNodeClearVariables(LogicNodeActionType):
    bl_idname = "NLActionClearVariables"
    bl_label = "Clear Variables"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULClearVariables"
    bl_description = 'Remove all saved variables from an external file'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'path', 'file_name']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
