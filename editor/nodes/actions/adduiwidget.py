from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeAddUIWidget(LogicNodeActionType):
    bl_idname = "LogicNodeAddUIWidget"
    bl_label = "Add Widget"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicUI, "Widget")
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    nl_class = "ULAddUIWidget"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", 'parent_widget', 'child_widget']
