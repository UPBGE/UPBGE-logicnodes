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
    bl_description = 'Keyboard activity'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULKeyLogger"

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, 'Only Characters', 'only_characters', {'default_value': True})
        self.add_output(NodeSocketLogicCondition, "Pressed", 'PRESSED')
        self.add_output(NodeSocketLogicString, "Character", 'CHARACTER')
        self.add_output(NodeSocketLogicString, "Keycode", 'KEYCODE')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["only_characters"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["PRESSED", "CHARACTER", "KEYCODE"]
