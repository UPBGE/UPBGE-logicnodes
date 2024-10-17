from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloat
from ....utilities import WARNING_MESSAGES


@node_type
class LogicNodeGamepadTrigger(LogicNodeParameterType):
    bl_idname = "NLGamepadTriggerCondition"
    bl_label = "Gamepad Trigger"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = ''
    deprecated = True
    deprecation_message = 'Included in "Gamepad Button" node'

    def init(self, context):
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloat, 'Sensitivity', None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, 'Threshold', None, {'default_value': 0.05})
        self.add_output(NodeSocketLogicFloat, "Left Trigger")
        self.add_output(NodeSocketLogicFloat, "Right Trigger")
        LogicNodeParameterType.init(self, context)

    def check(self, tree):
        super().check(tree)
        if len(self.outputs) < 2:
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(f"Node '{self.name}' in tree '{tree.name}' changed outputs. Re-Add to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)

    nl_class = "ULGamepadTrigger"

    def get_input_names(self):
        return ["index", 'sensitivity', 'threshold']

    def get_output_names(self):
        return ["LEFT", "RIGHT"]
