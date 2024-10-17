from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeControllerStatus(LogicNodeConditionType):
    bl_idname = "NLControllerStatus"
    bl_label = "Controller Status"
    bl_description = 'Return the status of a Controller type logic brick'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULControllerStatus"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object', 'obj_name')
        self.add_input(NodeSocketLogicBrick, 'Controller', 'cont_name', {'brick_type': 'controllers'})
        self.add_output(NodeSocketLogicCondition, "Status", 'OUT')
        self.add_output(NodeSocketLogicDictionary, "Sensors", 'SENSORS')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['obj_name', 'cont_name']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT', 'SENSORS']
