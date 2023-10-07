from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty


@node_type
class LogicNodeMouseMoved(LogicNodeConditionType):
    bl_idname = "NLMouseMovedCondition"
    bl_label = "Moved"
    bl_icon = 'MOUSE_MOVE'
    nl_category = "Input"
    nl_subcat = 'Mouse'
    nl_module = 'conditions'

    search_tags = [
        ['Mouse Moved', {}]
    ]

    pulse: BoolProperty(default=False)

    def init(self, context):
        self.add_output(NodeSocketLogicCondition, "If Moved")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Each Frame")

    nl_class = "ULMouseMoved"

    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [("pulse", self.pulse)]
