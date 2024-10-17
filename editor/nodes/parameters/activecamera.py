from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeActiveCamera(LogicNodeParameterType):
    bl_idname = "NLActiveCameraParameterNode"
    bl_label = "Active Camera"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = 'The current camera used to render the scene'
    nl_class = "ULActiveCamera"

    def init(self, context):
        self.add_output(NodeSocketLogicObject, "Camera", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
