from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeShowFramerate(LogicNodeActionType):
    bl_idname = "NLShowFramerate"
    bl_label = "Show Framerate"
    bl_description = 'Show the framerate in the top left corner'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULShowFramerate"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicBoolean, 'Show', 'use_framerate')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "use_framerate"]
