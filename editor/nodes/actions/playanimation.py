from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicAnimation
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicPlayMode
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBlendMode
from ...sockets import NodeSocketLogicFloatFactor
from bpy.props import BoolProperty


@node_type
class LogicNodePlayAnimation(LogicNodeActionType):
    bl_idname = "NLActionPlayActionNode"
    bl_label = "Play Animation"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPlayAction"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object / Armature")
        self.add_input(NodeSocketLogicAnimation, "Action")
        self.add_input(NodeSocketLogicFloat, "Start")
        self.add_input(NodeSocketLogicFloat, "End")
        self.add_input(NodeSocketLogicIntegerPositive, "Layer")
        self.add_input(NodeSocketLogicIntegerPositive, "Priority")
        self.add_input(NodeSocketLogicPlayMode, "Play Mode")
        self.add_input(NodeSocketLogicBoolean, "Stop When Done", {'value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Layer Weight", {'value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Blendin")
        self.add_input(NodeSocketLogicBlendMode, "Blend Mode")
        self.add_output(NodeSocketLogicCondition, "Started")
        self.add_output(NodeSocketLogicCondition, "Running")
        self.add_output(NodeSocketLogicCondition, "On Finish")
        self.add_output(NodeSocketLogicFloat, "Current Frame")
        LogicNodeActionType.init(self, context)


    def get_input_names(self):
        # XXX: Legacy Check
        for i in self.inputs:
            i.enabled = True
        return [
            "condition",
            "game_object",
            "action_name",
            "start_frame",
            "end_frame",
            "layer",
            "priority",
            "play_mode",
            "stop",
            "layer_weight",
            "speed",
            "blendin",
            "blend_mode"
        ]

    def get_output_names(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]
