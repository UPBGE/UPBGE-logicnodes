from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicGlobalCategory
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeListGlobalValues(LogicNodeActionType):
    bl_idname = "NLActionListGlobalValues"
    bl_label = "List Global Category"
    bl_description = 'Collect info about all saved properties in a global category'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULListGlobalValues"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicGlobalCategory, "Category", 'data_id')
        self.add_input(NodeSocketLogicBoolean, 'Print', 'print_d')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicDictionary, "Value", 'VALUE')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', "data_id", 'print_d']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "VALUE"]
