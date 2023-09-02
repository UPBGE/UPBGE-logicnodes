from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeCreateUICanvas(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUICanvas"
    bl_label = "Create Canvas"
    nl_category = "UI"
    nl_module = 'actions'

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Canvas")

    def get_netlogic_class_name(self):
        return "ULCreateUICanvas"

    def get_output_names(self):
        return ["OUT", 'CANVAS']

    def get_input_names(self):
        return ["condition"]
