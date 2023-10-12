from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatAngle
from ...enum_types import _enum_local_axis
from ...enum_types import _rotate_by_types
from bpy.props import EnumProperty


@node_type
class LogicNodeRotateByPoint(LogicNodeParameterType):
    bl_idname = "LogicNodeRotateByPoint"
    bl_label = "Rotate By Point"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULRotateByPoint"

    def update_draw(self, context=None):
        self.inputs[3].enabled = self.mode == '2'

    mode: EnumProperty(items=_rotate_by_types, name='Mode', update=update_draw)
    global_axis: EnumProperty(items=_enum_local_axis)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')
        if self.mode == '1':
            layout.prop(self, 'global_axis', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Origin')
        self.add_input(NodeSocketLogicVectorXYZ, 'Pivot')
        self.add_input(NodeSocketLogicFloatAngle, 'Angle')
        self.add_input(NodeSocketLogicVectorXYZ, 'Axis')
        self.add_output(NodeSocketLogicVectorXY, 'Point')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["origin", "pivot", 'angle', 'arbitrary_axis']

    def get_attributes(self):
        return [
            ('mode', self.mode),
            ('global_axis', self.global_axis)
        ]

    def get_output_names(self):
        return ["OUT"]
