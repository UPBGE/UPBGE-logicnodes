from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicIntegerPositive


@node_type
class LogicNodeAnimationStatus(LogicNodeParameterType):
    bl_idname = "NLParameterActionStatus"
    bl_label = "Animation Status"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = 'Information about an action in object context'
    nl_class = "ULActionStatus"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicIntegerPositive, "Layer", 'action_layer')
        self.add_output(NodeSocketLogicCondition, "Is Playing", 'OUT')
        self.add_output(NodeSocketLogicString, "Action Name", 'ACTION_NAME')
        self.add_output(NodeSocketLogicFloat, "Action Frame", 'ACTION_FRAME')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object", "action_layer"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT', "ACTION_NAME", "ACTION_FRAME"]
