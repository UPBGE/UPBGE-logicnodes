from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicObjectName


@node_type
class LogicNodeChildByName(LogicNodeParameterType):
    bl_idname = "NLParameterFindChildByNameNode"
    bl_label = "Get Child By Name"
    bl_icon = 'COMMUNITY'
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Parent')
        self.add_input(NodeSocketLogicObjectName, 'Child')
        self.add_output(NodeSocketLogicObject, 'Child')
        LogicNodeParameterType.init(self, context)

    nl_class = "ULChildByName"

    def get_input_names(self):
        return ["from_parent", "child"]

    def get_output_names(self):
        return ['CHILD']
