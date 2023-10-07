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
    nl_module = 'conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBrick, 'Controller', {'brick_type': 'controllers'})
        self.add_output(NodeSocketLogicCondition, "Status")
        self.add_output(NodeSocketLogicDictionary, "Sensors")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULControllerStatus"

    def get_input_names(self):
        return ['obj_name', 'cont_name']

    def get_output_names(self):
        return ['OUT', 'SENSORS']
