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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicScene, "Scene")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'scene']

    def get_output_names(self):
        return ['OUT']
