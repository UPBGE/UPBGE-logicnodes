from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicKeyboardKey
from ...sockets import NodeSocketLogicInteger
from bpy.props import StringProperty


@node_type
class LogicNodeKeyCode(LogicNodeParameterType):
    bl_idname = "NLParameterKeyboardKeyCode"
    bl_label = "Key Code"
    nl_module = 'uplogic.nodes.parameters'

    value: StringProperty()

    def init(self, context):
        self.add_input(NodeSocketLogicKeyboardKey, "")
        self.add_output(NodeSocketLogicInteger, "Code")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["key_code"]

    nl_class = "ULKeyCode"
