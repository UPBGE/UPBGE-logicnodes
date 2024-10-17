from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCamera


@node_type
class LogicNodeScreenPosition(LogicNodeParameterType):
    bl_idname = "NLParameterScreenPosition"
    bl_label = "World To Screen"
    bl_description = 'Determine the position of a point on screen'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULScreenPosition"

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Point', 'game_object')
        self.add_input(NodeSocketLogicCamera, 'Camera', 'camera', {'use_active': True})
        self.add_output(NodeSocketLogicVectorXY, 'On Screen', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object", "camera"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
