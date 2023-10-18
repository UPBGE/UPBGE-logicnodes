from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicGlobalCategory
from ...sockets import NodeSocketLogicGlobalProperty
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetGlobalValue(LogicNodeActionType):
    bl_idname = "NLActionSetGlobalValue"
    bl_label = "Set Global Value"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGlobalValue"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", {'show_prop': True})
        self.add_input(NodeSocketLogicGlobalCategory, "Category")
        self.add_input(NodeSocketLogicGlobalProperty, "Property", {'ref_index': 1})
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "Persistent")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "data_id", "key", "value", 'persistent']
