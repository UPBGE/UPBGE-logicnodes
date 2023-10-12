from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetSensorValue(LogicNodeActionType):
    bl_idname = "NLSetSensorValueNode"
    bl_label = "Set Sensor Value"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBrick, "Sensor", {'ref_index': 1, 'brick_type': 'sensors'})
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULSetSensorValue"

    def get_input_names(self):
        return ["condition", 'game_obj', 'sens_name', 'field', 'value']
