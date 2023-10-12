from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeCreateUICanvas(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUICanvas"
    bl_label = "Create Canvas"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Canvas")
        LogicNodeActionType.init(self, context)

    nl_class = "ULCreateUICanvas"

    def get_output_names(self):
        return ["OUT", 'CANVAS']

    def get_input_names(self):
        return ["condition"]
