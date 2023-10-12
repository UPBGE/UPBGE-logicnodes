from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeSetResolution(LogicNodeActionType):
    bl_idname = "NLActionSetResolution"
    bl_label = "Set Resolution"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetResolution"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicInteger, 'X', {'value': 1920})
        self.add_input(NodeSocketLogicInteger, 'Y', {'value': 1080})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "x_res", 'y_res']
