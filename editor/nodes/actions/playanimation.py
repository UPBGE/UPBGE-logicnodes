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


@node_type
class LogicNodePlayAnimation(LogicNodeActionType):
    bl_idname = "NLActionPlayActionNode"
    bl_label = "Play Animation"
    bl_description = 'Start an animation on an object or armature'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPlayAction"

    def update_draw(self, context=None):
        self.inputs[8].enabled = False
        self.inputs[6].enabled = False

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object / Armature", 'game_object')
        self.add_input(NodeSocketLogicAnimation, "Action", 'action_name')
        self.add_input(NodeSocketLogicFloat, "Start", 'start_frame')
        self.add_input(NodeSocketLogicFloat, "End", 'end_frame')
        self.add_input(NodeSocketLogicIntegerPositive, "Layer", 'layer')
        self.add_input(NodeSocketLogicIntegerPositive, "Priority", 'priority', {'enabled': False})
        self.add_input(NodeSocketLogicPlayMode, "Play Mode", 'play_mode')
        self.add_input(NodeSocketLogicBoolean, "Stop When Done", 'stop', {'default_value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Intensity", 'layer_weight', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", 'speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Blend-In", 'blendin')
        self.add_input(NodeSocketLogicBlendMode, "Blend Mode", 'blend_mode')
        self.add_output(NodeSocketLogicCondition, "Started", 'STARTED')
        self.add_output(NodeSocketLogicCondition, "Running", 'RUNNING')
        self.add_output(NodeSocketLogicCondition, "On Finish", 'FINISHED')
        self.add_output(NodeSocketLogicFloat, "Current Frame", 'FRAME')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        # XXX: Remove legacy Re-Enable Check
        self.inputs[8].enabled = False
        self.inputs[6].enabled = False
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

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]
