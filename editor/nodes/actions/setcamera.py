from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeSetCamera(LogicNodeActionType):
    bl_idname = "NLActionSetActiveCamera"
    bl_label = "Set Camera"
    bl_description = 'Set the active camera'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCamera"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Camera', 'camera')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "camera"]
