from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCamera


@node_type
class LogicNodeScreenPosition(LogicNodeParameterType):
    bl_idname = "NLParameterScreenPosition"
    bl_label = "World To Screen"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULScreenPosition"

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Point')
        self.add_input(NodeSocketLogicCamera, 'Camera', None, {'use_active': True})
        self.add_output(NodeSocketLogicVectorXY, 'On Screen')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["game_object", "camera"]

    def get_output_names(self):
        return ["OUT"]
