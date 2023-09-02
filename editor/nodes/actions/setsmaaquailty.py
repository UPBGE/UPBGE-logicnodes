from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeSetSMAAQuality(LogicNodeActionType):
    bl_idname = "NLSetEeveeSMAAQuality"
    bl_label = "Set SMAA Quality"
    nl_category = 'Render'
    nl_subcat = 'EEVEE Effects'
    nl_module = 'actions'
    deprecated = True

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicInteger, 'Quality')
        self.add_output(NodeSocketLogicCondition, 'Done')

    def get_output_names(self):
        return ["OUT"]

    def get_netlogic_class_name(self):
        return "ULSetEeveeSMAAQuality"

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]
