from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicGameProperty
from ...enum_types import _enum_object_property_types
from bpy.props import EnumProperty


@node_type
class LogicNodeGetProperty(LogicNodeParameterType):
    bl_idname = "NLGameObjectPropertyParameterNode"
    bl_label = "Get Property"
    bl_icon = 'EXPORT'
    nl_module = 'parameters'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicGameProperty, "Property")
        self.add_output(NodeSocketLogicParameter, "Property Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetProperty"

    def get_input_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", self.mode)]

    def get_output_names(self):
        return ['OUT']
