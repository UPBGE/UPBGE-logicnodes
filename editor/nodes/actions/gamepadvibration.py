
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicTime


@node_type
class LogicNodeGamepadVibration(LogicNodeActionType):
    bl_idname = "NLGamepadVibration"
    bl_label = "Vibration"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloatFactor, 'Left')
        self.add_input(NodeSocketLogicFloatFactor, 'Right')
        self.add_input(NodeSocketLogicTime, 'Time', {'value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    nl_class = "ULGamepadVibration"

    def get_input_names(self):
        return ['condition', 'index', 'left', 'right', 'time']

    def get_output_names(self):
        return ["DONE"]
