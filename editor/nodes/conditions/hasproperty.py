from ...enum_types import _enum_object_property_types
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeHasProperty(LogicNodeConditionType):
    bl_idname = "NLGameObjectHasPropertyParameterNode"
    bl_label = "Has Property"
    bl_icon = 'QUESTION'
    nl_module = 'conditions'

    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicString, "Name", {'value': 'prop'})
        self.add_output(NodeSocketLogicCondition, "If True")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULHasProperty"

    def get_input_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", self.mode)]

    def get_output_names(self):
        return ['OUT']