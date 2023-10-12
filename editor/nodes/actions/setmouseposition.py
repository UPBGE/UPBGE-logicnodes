from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetMousePosition(LogicNodeActionType):
    bl_idname = "NLActionSetMousePosition"
    bl_label = "Set Position"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMousePosition"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicFloat, "Screen X", {'value': 0.5})
        self.add_input(NodeSocketLogicFloat, "Screen Y", {'value': 0.5})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "screen_x", "screen_y"]
