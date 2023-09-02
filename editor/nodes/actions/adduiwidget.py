from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeAddUIWidget(LogicNodeActionType):
    bl_idname = "LogicNodeAddUIWidget"
    bl_label = "Add Widget"
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicUI, "Widget")
        self.add_output(NodeSocketLogicCondition, "Done")

    def get_netlogic_class_name(self):
        return "ULAddUIWidget"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", 'parent_widget', 'child_widget']
