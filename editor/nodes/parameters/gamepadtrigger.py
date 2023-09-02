from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloat
from ....utilities import WARNING_MESSAGES
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeGamepadTrigger(LogicNodeParameterType):
    bl_idname = "NLGamepadTriggerCondition"
    bl_label = "Trigger"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloat, 'Sensitivity', {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, 'Threshold', {'value': 0.05})
        self.add_output(NodeSocketLogicFloat, "Left Trigger")
        self.add_output(NodeSocketLogicFloat, "Right Trigger")

    def check(self, tree):
        super().check(tree)
        if len(self.outputs) < 2:
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(f"Node '{self.name}' in tree '{tree.name}' changed outputs. Re-Add to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)

    def get_netlogic_class_name(self):
        return "ULGamepadTrigger"

    def get_input_names(self):
        return ["index", 'sensitivity', 'threshold']

    def get_output_names(self):
        return ["LEFT", "RIGHT"]
