from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicKeyboardKey
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty


@node_type
class LogicNodeKeyboardKeyUp(LogicNodeConditionType):
    bl_idname = "NLKeyReleasedCondition"
    bl_label = "Key Up"
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Key" Node.'

    pulse: BoolProperty(
        description=(
            'ON: True until the key is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=True)

    def init(self, context):
        self.add_input(NodeSocketLogicKeyboardKey, "")
        self.add_output(NodeSocketLogicCondition, "If Released")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Each Frame")

    nl_class = "ULKeyReleased"

    def get_input_names(self):
        return ["key_code"]

    def get_attributes(self):
        return [("pulse", self.pulse)]
