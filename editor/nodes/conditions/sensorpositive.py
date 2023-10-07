from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeSensorPositive(LogicNodeConditionType):
    bl_idname = "NLGetSensorNode"
    bl_label = "Sensor Positive"
    nl_module = 'conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBrick, 'Sensor', {'brick_type': 'sensors'})
        self.add_output(NodeSocketLogicCondition, "Positive")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULSensorPositive"

    def get_input_names(self):
        return ['obj_name', 'sens_name']

    def get_output_names(self):
        return ['OUT']
