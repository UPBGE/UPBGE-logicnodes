from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive


@node_type
class LogicNodeStopAnimation(LogicNodeActionType):
    bl_idname = "NLActionStopAnimation"
    bl_label = "Stop Animation"
    bl_description = 'Stop an action and free its layer'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStopAction"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicIntegerPositive, "Animation Layer", 'action_layer')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "action_layer"]
