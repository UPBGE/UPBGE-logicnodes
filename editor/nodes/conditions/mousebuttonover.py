from ...sockets import NodeSocketLogicMouseButton
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeMouseButtonOver(LogicNodeConditionType):
    bl_idname = "NLConditionMousePressedOn"
    bl_label = "Button Over"
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicMouseButton, "Mouse Button")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicCondition, "If True")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULMousePressedOn"

    def get_input_names(self):
        return ["mouse_button", "game_object"]

    def get_output_names(self):
        return ['OUT']
