from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFilePath
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSaveVariable(LogicNodeActionType):
    bl_idname = "NLActionSaveVariable"
    bl_label = "Save Variable"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSaveVariable"
    bl_description = 'Save a value in an external file'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicString, 'Name', 'name', {'default_value': 'var'})
        self.add_input(NodeSocketLogicValue, '', 'val')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'path', 'file_name', 'name', 'val']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
