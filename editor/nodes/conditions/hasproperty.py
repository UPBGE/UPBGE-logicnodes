from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_object_property_types
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeHasProperty(LogicNodeConditionType):
    bl_idname = "NLGameObjectHasPropertyParameterNode"
    bl_label = "Has Property"
    bl_icon = 'QUESTION'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'conditions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default='GAME',
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        LogicNodeConditionType.init(self, context)
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicString, "Name")
        self.inputs[-1].value = 'prop'
        self.add_output(NodeSocketLogicCondition, "If True")

    def get_netlogic_class_name(self):
        return "ULHasProperty"

    def get_input_names(self):
        return ["game_object", "property_name"]

    def get_attributes(self):
        return [("mode", lambda: f'"{self.mode}"')]

    def get_output_names(self):
        return ['OUT']