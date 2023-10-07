from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeInStream(LogicNodeParameterType):
    bl_idname = "NLKeyLoggerAction"
    bl_label = "Logger"
    nl_category = "Input"
    nl_subcat = 'Keyboard'
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, 'Only Characters', {'value': True})
        self.add_output(NodeSocketLogicCondition, "Pressed")
        self.add_output(NodeSocketLogicString, "Character")
        self.add_output(NodeSocketLogicString, "Keycode")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULKeyLogger"

    def get_input_names(self):
        return ["only_characters"]

    def get_output_names(self):
        return ["PRESSED", "CHARACTER", "KEYCODE"]
