from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicIntegerPositive
from ....utilities import OUTCELL


@node_type
class LogicNodeAnimationStatus(LogicNodeParameterType):
    bl_idname = "NLParameterActionStatus"
    bl_label = "Animation Status"
    nl_category = "Animation"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicIntegerPositive, "Layer")
        self.add_output(NodeSocketLogicCondition, "Is Playing")
        self.add_output(NodeSocketLogicString, "Action Name")
        self.add_output(NodeSocketLogicFloat, "Action Frame")

    def get_netlogic_class_name(self):
        return "ULActionStatus"

    def get_input_names(self):
        return ["game_object", "action_layer"]

    def get_output_names(self):
        return [OUTCELL, "ACTION_NAME", "ACTION_FRAME"]
