from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetCameraFOV(LogicNodeActionType):
    bl_idname = "NLActionSetCameraFov"
    bl_label = "Set FOV"
    nl_module = 'actions'
    nl_class = "ULSetCameraFOV"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Camera')
        self.add_input(NodeSocketLogicFloat, 'FOV')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "camera", 'fov']
