from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicScene


@node_type
class LogicNodeSetScene(LogicNodeActionType):
    bl_idname = "NLSetScene"
    bl_label = "Set Scene"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetScene"
    bl_description = 'Switch to another scene'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicScene, "Scene", 'scene')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'scene']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
