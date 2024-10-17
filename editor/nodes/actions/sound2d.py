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
    bl_description = 'Start a non-spacial sound'
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicSoundFile, "Sound File", 'sound')
        self.add_input(NodeSocketLogicLoopCount, "Mode", 'loop_count')
        self.add_input(NodeSocketLogicFloatPositive, "Pitch", 'pitch', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatFactor, "Volume", 'volume', {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale", 'ignore_timescale')
        self.add_output(NodeSocketLogicCondition, 'On Start', 'DONE')
        self.add_output(NodeSocketLogicCondition, 'On Finish', 'ON_FINISH')
        self.add_output(NodeSocketLogicPython, 'Sound', 'HANDLE')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "sound",
            "loop_count",
            "pitch",
            "volume",
            'ignore_timescale'
        ]
