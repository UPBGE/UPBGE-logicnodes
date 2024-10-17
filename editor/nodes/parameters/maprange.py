from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicParameter
from bpy.props import BoolProperty
from bpy.props import EnumProperty


_modes = [
    ('0', 'Float', ''),
    ('1', 'Vector', '')
]


@node_type
class LogicNodeMapRange(LogicNodeParameterType):
    bl_idname = "NLMapRangeNode"
    bl_label = "Map Range"
    bl_description = 'Map a value from one range to another'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULMapRange"

    def update_draw(self, context=None):
        mode = int(self.mode)
        self.inputs[0].enabled = not mode
        self.inputs[1].enabled = not mode
        self.inputs[2].enabled = not mode
        self.inputs[3].enabled = not mode
        self.inputs[4].enabled = not mode
        self.inputs[6].enabled = mode
        self.inputs[7].enabled = mode
        self.inputs[8].enabled = mode
        self.inputs[9].enabled = mode
        self.inputs[10].enabled = mode

    clamp: BoolProperty(name='Clamp')
    mode: EnumProperty(items=_modes, name='Mode', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicFloat, "From Min", 'from_min')
        self.add_input(NodeSocketLogicFloat, "From Max", 'from_max', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "To Min", 'to_min')
        self.add_input(NodeSocketLogicFloat, "To Max", 'to_max', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, 'Steps', 'steps', {'enabled': False})
        self.add_input(NodeSocketLogicVectorXYZ, "Value", 'value')
        self.add_input(NodeSocketLogicVectorXYZ, "From Min", 'from_min')
        self.add_input(NodeSocketLogicVectorXYZ, "From Max", 'from_max', {'default_value': (1.0, 1.0, 1.0)})
        self.add_input(NodeSocketLogicVectorXYZ, "To Min", 'to_min')
        self.add_input(NodeSocketLogicVectorXYZ, "To Max", 'to_max', {'default_value': (1.0, 1.0, 1.0)})
        self.add_input(NodeSocketLogicVectorXYZ, 'Steps', 'steps', {'enabled': False})
        self.add_output(NodeSocketLogicParameter, "Result", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')
        layout.prop(self, 'clamp')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "value",
            "from_min",
            "from_max",
            "to_min",
            "to_max",
            "steps",
            "value",
            "from_min",
            "from_max",
            "to_min",
            "to_max",
            "steps"
        ]

    def get_attributes(self):
        return [('clamp', self.clamp), ('mode', self.mode)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
