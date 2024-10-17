from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeLoadFileContent(LogicNodeActionType):
    bl_idname = "NLLoadFileContent"
    bl_label = "Load File Content"
    bl_description = 'Load the contents of the current file. This will not change the current scene'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULLoadFileContent"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_output(NodeSocketLogicCondition, 'Loaded', 'OUT')
        self.add_output(NodeSocketLogicCondition, 'Updated', 'UPDATED')
        self.add_output(NodeSocketLogicFloatFactor, 'Status', 'STATUS')
        self.add_output(NodeSocketLogicString, 'Datatype', 'DATATYPE')
        self.add_output(NodeSocketLogicString, 'Item', 'ITEM')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT', 'UPDATED', 'STATUS', 'DATATYPE', 'ITEM']
