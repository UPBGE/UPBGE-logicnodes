from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetMousePosition(LogicNodeActionType):
    bl_idname = "NLActionSetMousePosition"
    bl_label = "Set Cursor Position"
    bl_description = 'Set the position of the mouse cursor'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMousePosition"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicFloat, "Screen X", 'screen_x', {'default_value': 0.5})
        self.add_input(NodeSocketLogicFloat, "Screen Y", 'screen_y', {'default_value': 0.5})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "screen_x", "screen_y"]
