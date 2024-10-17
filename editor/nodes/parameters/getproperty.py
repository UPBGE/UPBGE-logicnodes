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
    bl_label = "Get Object Property"
    bl_description = 'Game property of an object'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetProperty"

    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicGameProperty, "Property", 'property_name')
        self.add_output(NodeSocketLogicParameter, "Property Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", self.mode)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
