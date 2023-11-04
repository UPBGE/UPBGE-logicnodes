from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from bpy.props import EnumProperty


_value_types = [
    ('0', 'Float', ''),
    ('1', 'Integer', ''),
    ('2', 'Boolean', ''),
    ('3', 'String', '')
]


@node_type
class LogicNodeSimpleValue(LogicNodeParameterType):
    bl_idname = "LogicNodeSimpleValue"
    bl_label = "Simple Value"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULSimpleValue"

    def update_draw(self, context=None):
        vtype = int(self.value_type)
        for i, e in enumerate(self.inputs):
            e.enabled = vtype is i
        for i, e in enumerate(self.outputs):
            e.enabled = vtype is i
        self.nl_label = self.search_tags[vtype][0]

    search_tags = [
        ('Float', {'nl_label': 'Float'}),
        ('Integer', {'nl_label': 'Integer'}),
        ('Boolean', {'nl_label': 'Boolean'}),
        ('String', {'nl_label': 'String'})
    ]

    value_type: EnumProperty(items=_value_types, name='Data Type', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Float")
        self.add_input(NodeSocketLogicInteger, "Integer")
        self.add_input(NodeSocketLogicBoolean, "Boolean")
        self.add_input(NodeSocketLogicString, "String")
        self.add_output(NodeSocketLogicFloat, "Float")
        self.add_output(NodeSocketLogicInteger, "Integer")
        self.add_output(NodeSocketLogicBoolean, "Boolean")
        self.add_output(NodeSocketLogicString, "String")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'value_type', text='')

    def get_input_names(self):
        return ["value", "value", "value", "value"]

    def get_output_names(self):
        return ["OUT", "OUT", "OUT", "OUT"]
