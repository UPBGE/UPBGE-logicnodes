from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from ...enum_types import _random_value_types
from bpy.props import EnumProperty


@node_type
class LogicNodeRandomValue(LogicNodeParameterType):
    bl_idname = "LogicNodeRandomValue"
    bl_label = "Random Value"
    bl_description = 'Randomly generated value. This node generates only one value per frame'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULRandomValue"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[0].enabled = self.inputs[1].enabled = self.outputs[0].enabled = self.data_type == '0'
        self.inputs[2].enabled = self.inputs[3].enabled = self.outputs[1].enabled = self.data_type == '1'
        self.inputs[4].enabled = self.inputs[5].enabled = self.outputs[2].enabled = self.data_type == '2'
        self.inputs[6].enabled = self.outputs[3].enabled = self.data_type == '3'
        self.nl_label = self.search_tags[int(self.data_type) + 1][0]

    data_type: EnumProperty(items=_random_value_types, name='Data Type', update=update_draw)

    search_tags = [
        ['Random Value', {}],
        ['Random Float', {'data_type': '0', 'nl_label': 'Random Float'}],
        ['Random Integer', {'data_type': '1', 'nl_label': 'Random Integer'}],
        ['Random Vector', {'data_type': '2', 'nl_label': 'Random Vector'}],
        ['Random Boolean', {'data_type': '3', 'nl_label': 'Random Boolean'}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Min", 'min_float')
        self.add_input(NodeSocketLogicFloat, "Max", 'max_float')
        self.add_input(NodeSocketLogicInteger, "Min", 'min_int')
        self.add_input(NodeSocketLogicInteger, "Max", 'max_int')
        self.add_input(NodeSocketLogicVectorXYZ, "Min", 'min_vector')
        self.add_input(NodeSocketLogicVectorXYZ, "Max", 'max_vector')
        self.add_input(NodeSocketLogicFloatFactor, "Probability", 'probability', {'default_value': .5})
        self.add_input(NodeSocketLogicInteger, "Seed", 'seed', {'enabled': False})
        self.add_output(NodeSocketLogicFloat, "Result", 'OUT')
        self.add_output(NodeSocketLogicInteger, "Result", 'OUT')
        self.add_output(NodeSocketLogicVectorXYZ, "Result", 'OUT')
        self.add_output(NodeSocketLogicBoolean, "Result", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'data_type', text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "min_float",
            "max_float",
            "min_int",
            "max_int",
            "min_vector",
            "max_vector",
            "probability",
            "seed"
        ]

    def get_attributes(self):
        return [
            ('data_type', self.data_type)
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'OUT', 'OUT', 'OUT']
