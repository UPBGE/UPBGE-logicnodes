
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicTime


@node_type
class LogicNodeGamepadVibration(LogicNodeActionType):
    bl_idname = "NLGamepadVibration"
    bl_label = "Gamepad Vibrate"
    bl_description = 'Activate vibration on a gamepad'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULGamepadVibration"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index', 'index')
        self.add_input(NodeSocketLogicFloatFactor, 'Left', 'left')
        self.add_input(NodeSocketLogicFloatFactor, 'Right', 'right')
        self.add_input(NodeSocketLogicTime, 'Time', 'time', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'index', 'left', 'right', 'time']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["DONE"]
