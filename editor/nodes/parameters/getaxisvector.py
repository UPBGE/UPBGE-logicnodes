from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_local_oriented_axis
from bpy.props import EnumProperty


@node_type
class LogicNodeGetAxisVector(LogicNodeParameterType):
    bl_idname = "NLParameterAxisVector"
    bl_label = "Get Axis Vector"
    bl_icon = 'EMPTY_ARROWS'
    nl_module = 'parameters'

    axis: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis
    )

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'axis', text='')

    nl_class = "ULAxisVector"

    def get_input_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("axis", self.axis)]

    def get_output_names(self):
        return ["OUT"]
