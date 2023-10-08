from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetObjectVisibility(LogicNodeActionType):
    bl_idname = "NLActionSetGameObjectVisibility"
    bl_label = "Set Visibility"
    nl_module = 'actions'
    nl_class = "ULSetVisibility"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBoolean, "Visible")
        self.add_input(NodeSocketLogicBoolean, "Include Children")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "visible", "recursive"]
