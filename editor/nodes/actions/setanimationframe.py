from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicAnimation
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetAnimationFrame(LogicNodeActionType):
    bl_idname = "NLActionSetAnimationFrame"
    bl_label = "Set Animation Frame"
    bl_description = 'Set the current frame of an animation'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetActionFrame"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicAnimation, "Action", 'action_name')
        self.add_input(NodeSocketLogicIntegerPositive, "Layer", 'action_layer')
        self.add_input(NodeSocketLogicFloatPositive, "Frame", 'action_frame')
        self.add_input(NodeSocketLogicBoolean, "Freeze", 'freeze', {'default_value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Layer Weight", 'layer_weight', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "action_layer",
            "action_frame",
            'freeze',
            'layer_weight'
        ]
