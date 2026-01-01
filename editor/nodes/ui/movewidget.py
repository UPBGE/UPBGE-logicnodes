from ..node import node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI
from bpy.props import EnumProperty

_move_operations = [
    ('0', 'Move to front', "Move the widget to the front of its parent widget's children"),
    ('1', 'Move up', "Move the widget one layer up amongst the parent widget's children"),
    ('2', 'Move down', "Move the widget one layer down amongst its parent widget's children"),
    ('3', 'Move to back', "Move the widget to the back of its parent widget's children")
]

@node_type
class LogicNodeMoveUIWidget(LogicNodeUIType):
    bl_idname = "LogicNodeMoveUIWidget"
    bl_label = "Move Widget"
    bl_description = 'Move a widget up or down in hierarchy'
    nl_module = 'uplogic.nodes.ui'
    nl_class = "MoveWidgetNode"

    mode: EnumProperty(items=_move_operations, name='Type')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Widget", 'widget')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeUIType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'mode', text='')

    def get_attributes(self):
        return [
            ("mode", repr(self.mode))
        ]
