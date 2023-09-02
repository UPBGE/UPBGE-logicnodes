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
    nl_category = 'Logic'
    nl_subcat = 'Bricks'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBrick, 'Sensor', {'brick_type': 'sensors'})
        self.add_input(NodeSocketLogicString, 'Field')
        self.add_output(NodeSocketLogicParameter, "Value")

    def get_netlogic_class_name(self):
        return "ULGetSensorValue"

    def get_input_names(self):
        return ['game_obj', 'sens_name', "field"]

    def get_output_names(self):
        return ['OUT']
