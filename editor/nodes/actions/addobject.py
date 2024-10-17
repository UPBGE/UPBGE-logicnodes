from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeAddObject(LogicNodeActionType):
    bl_idname = "NLAddObjectActionNode"
    bl_label = "Add Object"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAddObject"
    bl_description = 'Add an object into the scene. This object needs to be on an inactive view layer (invisible)'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object to Add", 'name', {'allow_owner': False})
        self.add_input(NodeSocketLogicObject, "Copy Transform", 'reference', description='Copy the transform matrix from this object')
        self.add_input(NodeSocketLogicIntegerPositive, "Life", 'life')
        self.add_input(NodeSocketLogicBoolean, "Full Copy", 'full_copy')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicObject, "Added Object", 'OBJ')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "name", 'reference', "life", 'full_copy']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT', 'OBJ']
