from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeInStream(LogicNodeParameterType):
    bl_idname = "NLKeyLoggerAction"
    bl_label = "Key Logger"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULKeyLogger"

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, 'Only Characters', None, {'default_value': True})
        self.add_output(NodeSocketLogicCondition, "Pressed")
        self.add_output(NodeSocketLogicString, "Character")
        self.add_output(NodeSocketLogicString, "Keycode")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["only_characters"]

    def get_output_names(self):
        return ["PRESSED", "CHARACTER", "KEYCODE"]
