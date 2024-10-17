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
    bl_label = "Set Global Property"
    bl_description = 'Save a value into a property that can be retrieved elsewhere'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGlobalValue"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition', {'show_prop': True})
        self.add_input(NodeSocketLogicGlobalCategory, "Category", 'data_id')
        self.add_input(NodeSocketLogicGlobalProperty, "Property", 'key', {'ref_index': 1})
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_input(NodeSocketLogicBoolean, "Persistent", 'persistent')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "data_id", "key", "value", 'persistent']
