from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicObject
from bpy.props import BoolProperty
from bpy.props import EnumProperty


_draw_types = [
    ('0', 'Line', ''),
    ('1', 'Arrow', ''),
    ('2', 'Path', ''),
    ('3', 'Cube', ''),
    ('4', 'Box', ''),
    ('5', 'Mesh', ''),
    ('6', 'Axis', '')
]


@node_type
class LogicNodeDraw(LogicNodeActionType):
    bl_idname = "LogicNodeDraw"
    bl_label = "Draw"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "DrawNode"
    bl_description = 'Draw debug info on the screen'

    def update_draw(self, context=None):
        mode = int(self.mode)
        ipts = self.inputs
        ipts[1].enabled = mode != 6
        ipts[2].enabled = mode not in [2, 5, 6]
        ipts[3].enabled = mode < 2
        ipts[4].enabled = mode == 2
        ipts[5].enabled = 2 < mode < 5
        ipts[6].enabled = mode in [4, 6]
        ipts[7].enabled = mode == 4
        ipts[8].enabled = mode in [5, 6]

    use_volume_origin: BoolProperty(
        name='Use Volume Origin',
        description='Offset the origin by half of the box dimensions on each axis',
        default=False
    )

    mode: EnumProperty(items=_draw_types, name='Shape', update=update_draw)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', text='')
        mode = int(self.mode)
        if 2 < mode < 5:
            layout.prop(self, "use_volume_origin")

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition', {'show_prop': True})
        self.add_input(NodeSocketLogicColorRGB, 'Color', 'color')
        self.add_input(NodeSocketLogicVectorXYZ, 'Origin', 'origin')
        self.add_input(NodeSocketLogicVectorXYZ, 'Target', 'target')
        self.add_input(NodeSocketLogicList, 'Points', 'points')
        self.add_input(NodeSocketLogicFloatPositive, 'Width', 'width', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, 'Length', 'length', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, 'Height', 'height', {'default_value': 1.0})
        self.add_input(NodeSocketLogicObject, 'Object', 'object')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [
            ("use_volume_origin", f'{self.use_volume_origin}'),
            ("mode", f'{self.mode}')
        ]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'color', 'origin', 'target', 'points', 'width', 'length', 'height', 'object']

