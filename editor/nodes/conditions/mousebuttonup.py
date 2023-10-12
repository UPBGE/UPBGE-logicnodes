from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicMouseButton
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty


@node_type
class LogicNodeMouseButtonUp(LogicNodeConditionType):
    bl_idname = "NLMouseReleasedCondition"
    bl_label = "Button Up"
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Mouse Button" Node.'

    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        ),
        default=False)

    def init(self, context):
        self.add_input(NodeSocketLogicMouseButton, "")
        self.add_output(NodeSocketLogicCondition, "If Released")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Each Frame")

    nl_class = "ULMouseReleased"

    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [("pulse", self.pulse)]

    def get_output_names(self):
        return ['OUT']
