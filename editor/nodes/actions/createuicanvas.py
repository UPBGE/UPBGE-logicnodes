from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI
from bpy.props import BoolProperty


@node_type
class LogicNodeCreateUICanvas(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUICanvas"
    bl_label = "Create Canvas"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUICanvas"

    def update_draw(self, context=None):
        self.inputs[0].enabled = not self.on_init

    on_init: BoolProperty(name='On Init', update=update_draw, default=True)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Canvas")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'on_init')

    def get_attributes(self):
        return [
            ('on_init', self.on_init)
        ]

    def get_output_names(self):
        return ["OUT", 'CANVAS']

    def get_input_names(self):
        return ["condition"]
