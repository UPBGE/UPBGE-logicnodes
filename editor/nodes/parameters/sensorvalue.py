from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeSensorValue(LogicNodeParameterType):
    bl_idname = "NLSensorValueNode"
    bl_label = "Get Sensor Value"
    bl_description = 'Retrieve a value from a sensor type logic brick'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetSensorValue"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object', 'game_obj')
        self.add_input(NodeSocketLogicBrick, 'Sensor', 'sens_name', {'brick_type': 'sensors'})
        self.add_input(NodeSocketLogicString, 'Field', 'field')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['game_obj', 'sens_name', "field"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
