from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeMouseOver(LogicNodeConditionType):
    bl_idname = "NLConditionMouseTargetingNode"
    bl_label = "Over"
    nl_module = 'conditions'

    search_tags = [
        ['Mouse Over', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicCondition, "On Enter")
        self.add_output(NodeSocketLogicCondition, "On Over")
        self.add_output(NodeSocketLogicCondition, "On Exit")
        self.add_output(NodeSocketLogicVectorXYZ, "Point")
        self.add_output(NodeSocketLogicVectorXYZ, "Normal")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULMouseOver"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return [
            "MOUSE_ENTERED",
            "MOUSE_OVER",
            "MOUSE_EXITED",
            "POINT",
            "NORMAL"
        ]
