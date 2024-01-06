from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVectorXYZVelocity


@node_type
class LogicNodeSetGravity(LogicNodeActionType):
    bl_idname = "NLActionSetGravity"
    bl_label = "Set Gravity"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGravity"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicVectorXYZVelocity, "Gravity", None, {'default_value': (0., 0., -9.8)})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "gravity"]
