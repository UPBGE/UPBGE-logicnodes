from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeAddUIWidget(LogicNodeActionType):
    bl_idname = "LogicNodeAddUIWidget"
    bl_label = "Add Widget"
    nl_module = 'uplogic.nodes.actions'
    bl_description = 'Add one widget to another. The child widget will then be drawn relative to the parent'
    nl_class = "ULAddUIWidget"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent_widget')
        self.add_input(NodeSocketLogicUI, "Widget", 'child_widget')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'parent_widget', 'child_widget']
