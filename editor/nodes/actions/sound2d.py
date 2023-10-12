from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicSoundFile
from ...sockets import NodeSocketLogicLoopCount
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicPython


@node_type
class LogicNodeSound2D(LogicNodeActionType):
    bl_idname = "NLActionStartSound"
    bl_label = "2D Sound"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStartSound"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicSoundFile, "Sound File")
        self.add_input(NodeSocketLogicLoopCount, "Mode")
        self.add_input(NodeSocketLogicFloatPositive, "Pitch", {'value': 1.0})
        self.add_input(NodeSocketLogicFloatFactor, "Volume", {'value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale")
        self.add_output(NodeSocketLogicCondition, 'On Start')
        self.add_output(NodeSocketLogicCondition, 'On Finish')
        self.add_output(NodeSocketLogicPython, 'Sound')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_input_names(self):
        return [
            "condition",
            "sound",
            "loop_count",
            "pitch",
            "volume",
            'ignore_timescale'
        ]
