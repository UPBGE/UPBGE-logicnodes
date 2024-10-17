from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicSpeaker
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicLoopCount
from ...sockets import NodeSocketLogicPython


@node_type
class LogicNodePlaySpeaker(LogicNodeActionType):
    bl_idname = "NLPlaySpeaker"
    bl_label = "Start Speaker"
    bl_description = 'Start a speaker using its properties'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStartSpeaker"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicSpeaker, "Speaker", 'speaker')
        self.add_input(NodeSocketLogicBoolean, "Use Occlusion", 'occlusion')
        self.add_input(NodeSocketLogicFloatFactor, 'Transition', 'transition', {'default_value': .1})
        self.add_input(NodeSocketLogicFloatFactor, 'Lowpass', 'cutoff', {'default_value': .1})
        self.add_input(NodeSocketLogicLoopCount, "Mode", 'loop_count')
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale", 'ignore_timescale')
        self.add_output(NodeSocketLogicCondition, 'On Start', 'DONE')
        self.add_output(NodeSocketLogicCondition, 'On Finish', 'ON_FINISH')
        self.add_output(NodeSocketLogicPython, 'Sound', 'HANDLE')
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        self.inputs[3].enabled = self.inputs[4].enabled = self.inputs[2].default_value

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "speaker",
            'occlusion',
            'transition',
            'cutoff',
            "loop_count",
            'ignore_timescale'
        ]
