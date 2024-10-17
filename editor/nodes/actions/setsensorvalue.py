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
    bl_description = 'Set a value on a sensor type logic brick by name'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetSensorValue"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_obj')
        self.add_input(NodeSocketLogicBrick, "Sensor", 'sens_name', {'ref_index': 1, 'brick_type': 'sensors'})
        self.add_input(NodeSocketLogicString, "Attribute", 'field')
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'game_obj', 'sens_name', 'field', 'value']
