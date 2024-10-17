from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeMouseOver(LogicNodeConditionType):
    bl_idname = "NLConditionMouseTargetingNode"
    bl_label = "Mouse Over"
    bl_description = 'Check if the mouse is hovering over an object'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = 'ULMouseOver'

    search_tags = [
        ['Mouse Over', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicCondition, "On Enter", 'MOUSE_ENTERED')
        self.add_output(NodeSocketLogicCondition, "On Over", 'MOUSE_OVER')
        self.add_output(NodeSocketLogicCondition, "On Exit", 'MOUSE_EXITED')
        self.add_output(NodeSocketLogicVectorXYZ, "Point", 'POINT')
        self.add_output(NodeSocketLogicVectorXYZ, "Normal", 'NORMAL')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return [
            "MOUSE_ENTERED",
            "MOUSE_OVER",
            "MOUSE_EXITED",
            "POINT",
            "NORMAL"
        ]
