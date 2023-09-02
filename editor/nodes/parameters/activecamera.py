from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeActiveCamera(LogicNodeParameterType):
    bl_idname = "NLActiveCameraParameterNode"
    bl_label = "Active Camera"
    nl_category = "Scene"
    nl_subcat = 'Camera'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicObject, "Camera")

    def get_netlogic_class_name(self):
        return "ULActiveCamera"

    def get_output_names(self):
        return ["OUT"]
