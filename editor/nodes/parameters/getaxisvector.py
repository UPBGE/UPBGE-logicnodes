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
    bl_description = 'Direction of a local object axis'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULAxisVector"

    axis: EnumProperty(
        name='Axis',
        items=_enum_local_oriented_axis
    )

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'axis', text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("axis", self.axis)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
