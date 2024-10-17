from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeRemoveVariable(LogicNodeActionType):
    bl_idname = "NLActionRemoveVariable"
    bl_label = "Remove Variable"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveVariable"
    bl_description = 'Remove a previously saved variable from a file'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicString, 'Name', 'name', {'default_value': 'var'})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'path', 'file_name', 'name']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
