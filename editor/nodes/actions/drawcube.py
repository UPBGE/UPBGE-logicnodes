from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive
from bpy.props import BoolProperty


@node_type
class LogicNodeDrawCube(LogicNodeActionType):
    bl_idname = "NLDrawCube"
    bl_label = "Draw Cube"
    nl_module = 'uplogic.nodes.actions'
    nl_class = 'ULDrawCube'
    
    deprecated = True

    use_volume_origin: BoolProperty(
        name='Use Volume Origin',
        description='Offset the origin by half of the cube width on each axis',
        default=False
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "use_volume_origin")

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition', {'show_prop': True})
        self.add_input(NodeSocketLogicColorRGB, 'Color', 'color')
        self.add_input(NodeSocketLogicVectorXYZ, 'Origin', 'origin')
        self.add_input(NodeSocketLogicFloatPositive, 'Width', 'width', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [("use_volume_origin", self.use_volume_origin)]

    def get_input_names(self):
        return ['condition', 'color', 'origin', 'width']

    def get_output_names(self):
        return ['OUT']
