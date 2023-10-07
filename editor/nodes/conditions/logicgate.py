from bpy.types import Context, UILayout
from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type
from ...enum_types import _logic_gates
from bpy.props import EnumProperty


@node_type
class LogicNodeLogicGate(LogicNodeConditionType):
    bl_idname = "LogicNodeLogicGate"
    bl_label = "Gate"
    bl_width_min = 60
    nl_module = 'conditions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[1].enabled = self.gate != '3'

    gate: EnumProperty(items=_logic_gates, name='Gate Type', update=update_draw)

    search_tags = [
        ['Logic Gate', {}],
        ['And', {'width': 80, 'hide': True, 'nl_label': 'And'}],
        ['Or', {'gate': '1', 'width': 80, 'hide': True, 'nl_label': 'Or'}],
        ['Xor', {'gate': '2', 'width': 80, 'hide': True, 'nl_label': 'Xor'}],
        ['Not', {'gate': '3', 'width': 80, 'hide': True, 'nl_label': 'Not'}],
        ['Nand', {'gate': '4', 'width': 80, 'hide': True, 'nl_label': 'Nand'}],
        ['Nor', {'gate': '5', 'width': 80, 'hide': True, 'nl_label': 'Nor'}],
        ['Xnor', {'gate': '6', 'width': 80, 'hide': True, 'nl_label': 'Xnor'}],
        ['And Not', {'gate': '7', 'width': 90, 'hide': True, 'nl_label': 'And Not'}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "A")
        self.add_input(NodeSocketLogicCondition, "B")
        self.add_output(NodeSocketLogicCondition, "Result")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'gate', text='')

    nl_class = "ULLogicGate"

    def get_attributes(self):
        return [("gate", self.gate)]

    def get_output_names(self):
        return ['OUT']

    def get_input_names(self):
        return ["ca", "cb"]
