from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetActuatorValue(LogicNodeActionType):
    bl_idname = "NLSetActuatorValueNode"
    bl_label = "Set Actuator Value"
    bl_description = 'Set a value on an actuator type logic brick by name'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetActuatorValue"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_obj')
        self.add_input(NodeSocketLogicBrick, "Actuator", 'act_name', {'ref_index': 1, 'brick_type': 'actuators'})
        self.add_input(NodeSocketLogicString, "Attribute", 'field')
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]


    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'game_obj', 'act_name', 'field', 'value']
