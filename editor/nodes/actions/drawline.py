from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeDrawLine(LogicNodeActionType):
    bl_idname = "NLDrawLine"
    bl_label = "Draw Line"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULDrawLine"

    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', None, {'show_prop': True})
        self.add_input(NodeSocketLogicColorRGB, 'Color')
        self.add_input(NodeSocketLogicVectorXYZ, 'From')
        self.add_input(NodeSocketLogicVectorXYZ, 'To')
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'color', 'from_point', 'to_point']

