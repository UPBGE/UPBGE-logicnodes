from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicVectorXYZAngle
from bpy.props import EnumProperty
from ....utilities import WARNING_MESSAGES


@node_type
class LogicNodeRotateByPoint(LogicNodeParameterType):
    bl_idname = "LogicNodeRotateByPoint"
    bl_label = "Vector Rotate"
    bl_description = 'Rotational operation on vectors'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULRotateByPoint"

    def update_draw(self, context=None):
        # XXX: Remove Legacy Check
        mode = int(self.mode)
        if len(self.inputs) == 4:
            self.inputs[3].enabled = mode == 2
        elif len(self.inputs) == 5:
            self.inputs[2].enabled = mode == 2
            self.inputs[3].enabled = mode != 3
            self.inputs[4].enabled = mode == 3
        else:
            self.inputs[0].enabled = mode == 0
            self.inputs[1].enabled = mode == 0
            self.inputs[2].enabled = mode != 0
            self.inputs[3].enabled = mode != 0
            self.inputs[4].enabled = mode == 2
            self.inputs[5].enabled = mode != 3
            self.inputs[6].enabled = mode == 3

    axis_options = [
        ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
        ("1", "Y Axis", "The Local Y Axis [Integer Value 1]"),
        ("2", "Z Axis", "The Local Z Axis [Integer Value 2]")
    ]

    rotate_options = [
        ("0", "2D", ""),
        ("1", "3D", ""),
        ("2", "Arbitrary Axis", ""),
        ("3", "Euler", "")
    ]

    mode: EnumProperty(items=rotate_options, name='Mode', update=update_draw)
    global_axis: EnumProperty(items=axis_options, name='Axis')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')
        if self.mode == '1':
            layout.prop(self, 'global_axis', text='')
    
    def check(self, tree):
        super().check(tree)
        if len(self.inputs) < 7:
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(f"Node '{self.name}' in tree '{tree.name}' changed inputs. Re-Add to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXY, 'Origin', 'origin', {'align': False})
        self.add_input(NodeSocketLogicVectorXY, 'Pivot', 'pivot', {'align': False})
        self.add_input(NodeSocketLogicVectorXYZ, 'Origin', 'origin')
        self.add_input(NodeSocketLogicVectorXYZ, 'Pivot', 'pivot')
        self.add_input(NodeSocketLogicVectorXYZ, 'Axis', 'arbitrary_axis', {'default_value': (0, 0, 1)})
        self.add_input(NodeSocketLogicFloatAngle, 'Angle', 'angle')
        self.add_input(NodeSocketLogicVectorXYZAngle, 'Euler', 'euler_angles')
        self.add_output(NodeSocketLogicVectorXYZ, 'Point', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["origin", "pivot", "origin", "pivot", 'arbitrary_axis', 'angle', 'euler_angles']

    def get_attributes(self):
        return [
            ('mode', self.mode),
            ('global_axis', self.global_axis)
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
