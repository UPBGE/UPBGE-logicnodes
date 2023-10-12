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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULListGlobalValues"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicGlobalCategory, "Category")
        self.add_input(NodeSocketLogicBoolean, 'Print')
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicDictionary, "Value")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', "data_id", 'print_d']

    def get_output_names(self):
        return ["OUT", "VALUE"]
