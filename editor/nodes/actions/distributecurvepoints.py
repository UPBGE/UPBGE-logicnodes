from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicInteger
from ...sockets.curvesocket import NodeSocketLogicCurve
from bpy.props import BoolProperty


@node_type
class LogicNodeDistributeCurvePoints(LogicNodeActionType):
    bl_idname = "LogicNodeDistributeCurvePoints"
    bl_label = "Distribute Points on Curve"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "DistributeCurvePointsNode"
    bl_description = 'Distribute points along a curve using its resolution'

    def update_draw(self, context=None):
        self.inputs[2].enabled = self.custom_density
    
    debug: BoolProperty(
        name='Show Debug',
        description='Place wireframe cubes at the calculated points during runtime'
    )
    custom_density: BoolProperty(
        name='Custom Amount',
        description='Customize how many points to distribute along the curve',
        update=update_draw
    )
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'debug')
        layout.prop(self, 'custom_density')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Refresh', 'condition')
        self.add_input(NodeSocketLogicCurve, 'Curve', 'curve')
        self.add_input(NodeSocketLogicInteger, 'Amount', 'density', {'default_value': 10, 'enabled': False})
        self.add_output(NodeSocketLogicCondition, 'Done', 'DONE')
        self.add_output(NodeSocketLogicVector, 'Points', 'POINTS')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [('debug', self.debug), ('custom_density', self.custom_density)]
