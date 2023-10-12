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
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBrick, "Actuator", {'ref_index': 1, 'brick_type': 'actuators'})
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULSetActuatorValue"

    def get_input_names(self):
        return ["condition", 'game_obj', 'act_name', 'field', 'value']
