from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetObjectVisibility(LogicNodeActionType):
    bl_idname = "NLActionSetGameObjectVisibility"
    bl_label = "Set Visibility"
    bl_description = "Set an object's visibility"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetVisibility"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicBoolean, "Visible", 'visible')
        self.add_input(NodeSocketLogicBoolean, "Include Children", 'recursive')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "visible", "recursive"]
