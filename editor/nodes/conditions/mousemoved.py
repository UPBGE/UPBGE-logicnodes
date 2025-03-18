from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty


@node_type
class LogicNodeMouseMoved(LogicNodeConditionType):
    bl_idname = "NLMouseMovedCondition"
    bl_label = "Mouse Moved"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULMouseMoved"

    search_tags = [
        ['Mouse Moved', {}]
    ]

    pulse: BoolProperty(default=False)

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "If Moved", 'OUT')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Each Frame")

    def get_attributes(self):
        return [("pulse", self.pulse)]
