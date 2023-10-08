from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeSetLightColor(LogicNodeActionType):
    bl_idname = "NLSetLightColorAction"
    bl_label = "Set Light Color"
    nl_module = 'actions'
    nl_class = "ULSetLightColor"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicLight, "Light Object")
        self.add_input(NodeSocketLogicColorRGB, "Color")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "color"
        ]
