from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeSensorPositive(LogicNodeConditionType):
    bl_idname = "NLGetSensorNode"
    bl_label = "Sensor Positive"
    bl_description = 'Check if a Sensor type logic brick evaluates to "True"'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULSensorPositive"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object', 'obj_name')
        self.add_input(NodeSocketLogicBrick, 'Sensor', 'sens_name', {'brick_type': 'sensors'})
        self.add_output(NodeSocketLogicCondition, "Positive", 'OUT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['obj_name', 'sens_name']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
