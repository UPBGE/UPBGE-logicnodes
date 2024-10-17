from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXYZVelocity


@node_type
class LogicNodeSetGravity(LogicNodeActionType):
    bl_idname = "NLActionSetGravity"
    bl_label = "Set Gravity"
    bl_description = 'Set the general downwards force'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGravity"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicVectorXYZVelocity, "Gravity", 'gravity', {'default_value': (0., 0., -9.8)})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "gravity"]
