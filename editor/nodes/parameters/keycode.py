from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicKeyboardKey
from ...sockets import NodeSocketLogicInteger
from bpy.props import StringProperty


@node_type
class LogicNodeKeyCode(LogicNodeParameterType):
    bl_idname = "NLParameterKeyboardKeyCode"
    bl_label = "Key Code"
    bl_description = 'Numeric representation of a keyboard key'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULKeyCode"

    value: StringProperty()

    def init(self, context):
        self.add_input(NodeSocketLogicKeyboardKey, "", 'key_code')
        self.add_output(NodeSocketLogicInteger, "Code", 'OUT')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["key_code"]
