from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight


@node_type
class LogicNodeLightMakeUnique(LogicNodeActionType):
    bl_idname = "NLMakeUniqueLight"
    bl_label = "Make Light Unique"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMakeUniqueLight"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicLight, 'Light Object')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicLight, 'Light')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", 'LIGHT']

    def get_input_names(self):
        return [
            "condition",
            "light",
        ]
