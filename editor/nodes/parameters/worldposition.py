from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeWorldPosition(LogicNodeParameterType):
    bl_idname = "NLParameterWorldPosition"
    bl_label = "Screen To World"
    bl_description = 'Project a point on scree into the scene'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULWorldPosition"

    def init(self, context):
        self.add_input(NodeSocketLogicCamera, "Camera", 'camera', {'use_active': True})
        self.add_input(NodeSocketLogicFloat, "Screen X", 'screen_x')
        self.add_input(NodeSocketLogicFloat, "Screen Y", 'screen_y')
        self.add_input(NodeSocketLogicFloat, "Depth", 'world_z')
        self.add_output(NodeSocketLogicVectorXYZ, "World Position", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["camera", "screen_x", "screen_y", "world_z"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
