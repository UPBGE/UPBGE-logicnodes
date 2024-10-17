from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetCameraFOV(LogicNodeActionType):
    bl_idname = "NLActionSetCameraFov"
    bl_label = "Set FOV"
    bl_description = 'Set the Field of View on a perspective camera'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCameraFOV"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicCamera, 'Camera', 'camera')
        self.add_input(NodeSocketLogicFloat, 'FOV', 'fov')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "camera", 'fov']
