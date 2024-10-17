from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBrick


@node_type
class LogicNodeGetActuatorValue(LogicNodeParameterType):
    bl_idname = "NLGetActuatorValue"
    bl_label = "Get Actuator Value"
    bl_description = 'Named attribute of an actuator type logic brick'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetActuatorValue"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_obj')
        self.add_input(NodeSocketLogicBrick, "Actuator", 'act_name', {'brick_type': 'actuators'})
        self.add_input(NodeSocketLogicString, "Field", 'field')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_obj", "act_name", 'field']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
