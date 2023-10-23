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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object to Add", {'allow_owner': False})
        self.add_input(NodeSocketLogicObject, "Copy Data From (Optional)")
        self.add_input(NodeSocketLogicIntegerPositive, "Life")
        self.add_input(NodeSocketLogicBoolean, "Full Copy")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicObject, "Added Object")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition", "name", 'reference', "life", 'full_copy']

    def get_output_names(self):
        return ['OUT', 'OBJ']
