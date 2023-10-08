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
    nl_category = "Animation"
    nl_module = 'actions'
    nl_class = "ULSetActionFrame"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicAnimation, "Action")
        self.add_input(NodeSocketLogicIntegerPositive, "Layer")
        self.add_input(NodeSocketLogicFloatPositive, "Frame")
        self.add_input(NodeSocketLogicBoolean, "Freeze", {'value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Layer Weight", {'value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

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
