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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStartSpeaker"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicSpeaker, "Speaker")
        self.add_input(NodeSocketLogicBoolean, "Use Occlusion")
        self.add_input(NodeSocketLogicFloatFactor, 'Transition', {'value': .1})
        self.add_input(NodeSocketLogicFloatFactor, 'Lowpass', {'value': .1})
        self.add_input(NodeSocketLogicLoopCount, "Mode")
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale")
        self.add_output(NodeSocketLogicCondition, 'On Start')
        self.add_output(NodeSocketLogicCondition, 'On Finish')
        self.add_output(NodeSocketLogicPython, 'Sound')
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        self.inputs[3].enabled = self.inputs[4].enabled = self.inputs[2].value

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

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
