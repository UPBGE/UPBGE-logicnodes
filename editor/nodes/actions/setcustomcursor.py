from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeSetCustomCursor(LogicNodeActionType):
    bl_idname = "LogicNodeSetCustomCursor"
    bl_label = "Set Custom Cursor"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicImage, "Texture")
        self.add_input(NodeSocketLogicVectorXY, "Size", {'default_value': (30., 30.)})
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Cursor")
        LogicNodeActionType.init(self, context)

    nl_class = "ULSetCustomCursor"

    def get_output_names(self):
        return ["OUT", 'CURSOR']

    def get_input_names(self):
        return ["condition", "texture", "size"]
