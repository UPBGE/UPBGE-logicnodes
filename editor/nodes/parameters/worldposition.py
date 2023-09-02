from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeWorldPosition(LogicNodeParameterType):
    bl_idname = "NLParameterWorldPosition"
    bl_label = "World Position"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicCamera, "Camera", {'use_active': True})
        self.add_input(NodeSocketLogicFloat, "Screen X")
        self.add_input(NodeSocketLogicFloat, "Screen Y")
        self.add_input(NodeSocketLogicFloat, "Depth")
        self.add_output(NodeSocketLogicVectorXYZ, "World Position")

    def get_netlogic_class_name(self):
        return "ULWorldPosition"

    def get_input_names(self):
        return ["camera", "screen_x", "screen_y", "world_z"]

    def get_output_names(self):
        return ["OUT"]
