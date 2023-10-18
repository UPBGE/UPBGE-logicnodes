from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetCameraOrthoScale(LogicNodeActionType):
    bl_idname = "NLActionSetCameraOrthoScale"
    bl_label = "Set Orthographic Scale"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCameraOrthoScale"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Camera')
        self.add_input(NodeSocketLogicFloat, 'Scale', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "camera", 'scale']
