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
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicImage, "Texture")
        self.add_input(NodeSocketLogicVectorXY, "Size", {'value_x': 30, 'value_y': 30})
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Cursor")

    def get_netlogic_class_name(self):
        return "ULSetCustomCursor"

    def get_output_names(self):
        return ["OUT", 'CURSOR']

    def get_input_names(self):
        return ["condition", "texture", "size"]
