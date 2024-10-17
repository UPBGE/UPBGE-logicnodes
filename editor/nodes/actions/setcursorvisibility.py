from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetCursorVisibility(LogicNodeActionType):
    bl_idname = "NLActionSetMouseCursorVisibility"
    bl_label = "Cursor Visibility"
    bl_description = 'Set the visibility of the mouse cursor. This will only affect the system cursor, not custom ones'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCursorVisibility"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicBoolean, "Visible", 'visibility_status')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "visibility_status"]
