from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeChildByName(LogicNodeParameterType):
    bl_idname = "NLParameterFindChildByNameNode"
    bl_label = "Get Child By Name"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULChildByName"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Parent')
        self.add_input(NodeSocketLogicObject, 'Child', None, {'allow_owner': False})
        self.add_output(NodeSocketLogicObject, 'Child')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["from_parent", "child"]

    def get_output_names(self):
        return ['CHILD']
