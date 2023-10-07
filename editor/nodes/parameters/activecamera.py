from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeActiveCamera(LogicNodeParameterType):
    bl_idname = "NLActiveCameraParameterNode"
    bl_label = "Active Camera"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicObject, "Camera")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULActiveCamera"

    def get_output_names(self):
        return ["OUT"]
