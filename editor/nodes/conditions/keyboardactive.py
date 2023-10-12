from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition
from ....utilities import OUTCELL


@node_type
class LogicNodeKeyboardActive(LogicNodeConditionType):
    bl_idname = "NLKeyboardActive"
    bl_label = "Keyboard Active"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, 'Active')
        LogicNodeConditionType.init(self, context)

    nl_class = "ULKeyboardActive"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return [OUTCELL]
