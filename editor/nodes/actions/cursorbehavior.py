from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicBoolCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeCursorBehavior(LogicNodeActionType):
    bl_idname = "NLCursorBehavior"
    bl_label = "Cursor Behaviour"
    nl_category = "Scene"
    nl_module = 'actions'
    deprecated = True

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicBoolCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Cursor")
        self.add_input(NodeSocketLogicFloat, "Distance")
        self.add_output(NodeSocketLogicCondition, "Done")

    def get_netlogic_class_name(self):
        return "ULCursorBehavior"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "cursor_object", "world_z"]
