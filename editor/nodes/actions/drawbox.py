from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive
from bpy.props import BoolProperty


@node_type
class LogicNodeDrawBox(LogicNodeActionType):
    bl_idname = "NLDrawBox"
    bl_label = "Draw Box"
    nl_module = 'uplogic.nodes.actions'
    
    deprecated = True

    use_volume_origin: BoolProperty(
        name='Use Volume Origin',
        description='Offset the origin by half of the box dimensions on each axis',
        default=False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "use_volume_origin")

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', None, {'show_prop': True})
        self.add_input(NodeSocketLogicColorRGB, 'Color')
        self.add_input(NodeSocketLogicVectorXYZ, 'Origin')
        self.add_input(NodeSocketLogicFloatPositive, 'Width (X)', None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, 'Length (Y)', None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, 'Height (Z)', None, {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [("use_volume_origin", f'{self.use_volume_origin}')]

    def get_input_names(self):
        return ['condition', 'color', 'origin', 'width', 'length', 'height']

    nl_class = "ULDrawBox"
