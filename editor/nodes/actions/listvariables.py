from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListVariables(LogicNodeActionType):
    bl_idname = "NLActionListVariables"
    bl_label = "List Saved Variables"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULListVariables"
    bl_description = 'Collect info about all saved variables in a file'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition', {'show_prop': True})
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicBoolean, 'Print', 'print_list')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'path', 'file_name', 'print_list']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'LIST']
