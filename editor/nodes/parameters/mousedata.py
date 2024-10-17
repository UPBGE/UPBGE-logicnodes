from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicInteger
from bpy.props import EnumProperty
from bpy.props import BoolProperty


modes = [
    ('0', 'Position', ''),
    ('1', 'Movement', ''),
    ('2', 'Wheel', '')
]


@node_type
class LogicNodeMouseData(LogicNodeParameterType):
    bl_idname = "NLMouseDataParameter"
    bl_label = "Mouse Status"
    bl_description = 'Current status of the mouse'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULMouseData"

    search_tags = [
        ['Mouse Position', {'nl_label': 'Mouse Position', 'disable_out': [1, 4, 5, 6]}],
        ['Mouse Movement', {'nl_label': 'Mouse Movement', 'disable_out': [0, 2, 3, 6]}],
        ['Mouse Wheel', {'nl_label': 'Mouse Wheel', 'disable_out': [0, 1, 2, 3, 4, 5]}],
        ['Mouse Status', {}]
    ]

    def update_draw(self, context=None):
        mode = int(self.mode)
        self.outputs[0].enabled = mode == 0
        self.outputs[2].enabled = mode == 0
        self.outputs[3].enabled = mode == 0
        self.outputs[1].enabled = mode == 1
        self.outputs[4].enabled = mode == 1
        self.outputs[5].enabled = mode == 1
        self.outputs[6].enabled = mode == 2
        self.nl_label = modes[mode][1]

    mode: EnumProperty(name='Mode', items=modes, update=update_draw)
    invert_y: BoolProperty(name='Invert Y')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')
        layout.prop(self, 'invert_y')

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position", 'MXY0')
        self.add_output(NodeSocketLogicVectorXYZ, "Movement", 'MDXY0')
        self.add_output(NodeSocketLogicParameter, "X", 'MX')
        self.add_output(NodeSocketLogicParameter, "Y", 'MY')
        self.add_output(NodeSocketLogicParameter, "X", 'MDX')
        self.add_output(NodeSocketLogicParameter, "Y", 'MDY')
        self.add_output(NodeSocketLogicInteger, "Wheel Difference", 'MDWHEEL')
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        return [('invert_y', self.invert_y)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["MXY0", "MDXY0", "MX", "MY", "MDX", "MDY", "MDWHEEL"]
