from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetFullscreen(LogicNodeActionType):
    bl_idname = "NLActionSetFullscreen"
    bl_label = "Set Fullscreen"
    nl_category = 'Render'
    nl_module = 'actions'
    nl_class = "ULSetFullscreen"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicBoolean, 'Fullscreen')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "use_fullscreen"]
