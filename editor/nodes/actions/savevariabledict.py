from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeSaveVariableDict(LogicNodeActionType):
    bl_idname = "NLActionSaveVariables"
    bl_label = "Save Variable Dict"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSaveVariableDict"
    bl_description = 'Save a dictionary as an external file'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicDictionary, 'Variables', 'val')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'path', 'file_name', 'val']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
