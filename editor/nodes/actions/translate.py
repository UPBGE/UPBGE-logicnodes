from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTranslate(LogicNodeActionType):
    bl_idname = "NLActionTranslate"
    bl_label = "Translate"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULTranslate"
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBoolean, "Local")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_input(NodeSocketLogicFloat, "Speed", None, {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "When Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition", "moving_object", "local", "vect", "speed"]
