from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeChildByName(LogicNodeParameterType):
    bl_idname = "NLParameterFindChildByNameNode"
    bl_label = "Get Child By Name"
    bl_description = 'Child by name in the children of an object'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULChildByName"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Parent', 'from_parent')
        self.add_input(NodeSocketLogicObject, 'Child', 'child', {'allow_owner': False})
        self.add_output(NodeSocketLogicObject, 'Child', 'CHILD')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["from_parent", "child"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['CHILD']
