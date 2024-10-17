from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeSetLightColor(LogicNodeActionType):
    bl_idname = "NLSetLightColorAction"
    bl_label = "Set Light Color"
    bl_description = 'Set the color of a light'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetLightColor"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicLight, "Light Object", 'lamp')
        self.add_input(NodeSocketLogicColorRGB, "Color", 'color')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "color"
        ]
