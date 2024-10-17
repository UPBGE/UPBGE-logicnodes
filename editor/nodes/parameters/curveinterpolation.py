from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from bpy.props import PointerProperty
import bpy
import uuid


@node_type
class LogicNodeCurveInterpolation(LogicNodeParameterType):
    bl_idname = "LogicNodeCurveInterpolation"
    bl_label = "Curve Interpolation"
    bl_description = 'Map a value to a curve'
    bl_width_default = 200
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "CurveInterpolationNode"

    mapping: PointerProperty(name='Value', type=bpy.types.Brush)

    def draw_buttons(self, context, layout):
        if self.mapping.users > 2:
            layout.label(icon='ERROR', text='Data used in multiple nodes!')
        if self.mapping:
            layout.template_curve_mapping(self.mapping, 'curve')
        else:
            layout.label(icon='ERROR', text='Data not found!')

    def init(self, context):
        self.mapping = bpy.data.brushes.new(name=f'{uuid.uuid4()}')
        points = self.mapping.curve.curves[0].points
        points[0].location = (0, 0)
        points[1].location = (.25, .06)
        points[2].location = (.75, 0.94)
        points[3].location = (1, 1)
        self.mapping.curve.update()
        self.add_input(NodeSocketLogicFloatFactor, 'Value', 'value')
        self.add_output(NodeSocketLogicFloat, 'Value', 'OUT')
        LogicNodeParameterType.init(self, context)

    def free(self) -> None:
        if self.mapping and self.mapping.users == 2:
            bpy.data.brushes.remove(self.mapping)
        self.mapping = None

    def get_attributes(self):
        return [('mapping', f'bpy.data.brushes["{self.mapping.name}"]')]
