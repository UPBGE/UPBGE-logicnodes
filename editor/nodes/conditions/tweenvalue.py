from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import PointerProperty
from mathutils import Vector
import bpy
import uuid


value_types = [
    ('0', 'Float', 'Tween a floating point value'),
    ('1', 'Vector', 'Tween a vector value')
]


@node_type
class LogicNodeTweenValue(LogicNodeConditionType):
    bl_idname = "LogicNodeTweenValue"
    bl_label = "Tween Value"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "TweenValueNode"
    bl_width_default = 200

    def update_draw(self, context=None):
        self.inputs[0].enabled = not self.on_demand
        self.inputs[1].enabled = not self.on_demand

        self.inputs[2].enabled = not int(self.value_type)
        self.inputs[3].enabled = not int(self.value_type)
        self.inputs[4].enabled = int(self.value_type)
        self.inputs[5].enabled = int(self.value_type)

        self.outputs[0].enabled = not self.on_demand
        self.outputs[1].enabled = not self.on_demand

        self.outputs[2].enabled = not int(self.value_type)
        self.outputs[3].enabled = int(self.value_type)

    on_demand: BoolProperty(name='On Demand', description='Tween the value automatically when output socket is active', update=update_draw)
    instant_reset: BoolProperty(name='Instant Reset', description='Instantly reset the factor when the result is not being accessed')
    value_type: EnumProperty(name='Type', items=value_types, description='Value type to tween', update=update_draw)

    mapping: PointerProperty(name='Value', type=bpy.types.Brush)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value_type')
        layout.prop(self, 'on_demand')
        if self.on_demand:
            layout.prop(self, 'instant_reset')
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
        self.add_input(NodeSocketLogicCondition, 'Forward', 'forward')
        self.add_input(NodeSocketLogicCondition, 'Back', 'back')
        self.add_input(NodeSocketLogicFloat, 'From', 'from_float')
        self.add_input(NodeSocketLogicFloat, 'To', 'to_float', {'default_value': 1.0})
        self.add_input(NodeSocketLogicVectorXYZ, 'From', 'from_vec')
        self.add_input(NodeSocketLogicVectorXYZ, 'To', 'to_vec', {'default_value': Vector((1, 1, 1))})
        self.add_input(NodeSocketLogicFloat, 'Duration', 'duration', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done', 'DONE')
        self.add_output(NodeSocketLogicCondition, 'Reached', 'REACHED')
        self.add_output(NodeSocketLogicFloat, 'Result', 'RESULT_FLOAT')
        self.add_output(NodeSocketLogicVector, 'Result', 'RESULT_VEC')
        self.add_output(NodeSocketLogicFloat, 'Factor', 'FAC')
        LogicNodeConditionType.init(self, context)

    def free(self) -> None:
        if self.mapping and self.mapping.users == 2:
            bpy.data.brushes.remove(self.mapping)
        self.mapping = None

    def get_attributes(self):
        return [
            ('on_demand', self.on_demand),
            ('instant_reset', self.instant_reset),
            ('value_type', self.value_type),
            ('mapping', f'bpy.data.brushes["{self.mapping.name}"]')
        ]
