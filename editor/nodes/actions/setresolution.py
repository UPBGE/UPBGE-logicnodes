from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeSetResolution(LogicNodeActionType):
    bl_idname = "NLActionSetResolution"
    bl_label = "Set Resolution"
    bl_description = 'Set the screen resolution'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetResolution"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicInteger, 'X', 'x_res', {'default_value': 1920})
        self.add_input(NodeSocketLogicInteger, 'Y', 'y_res', {'default_value': 1080})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "x_res", 'y_res']
