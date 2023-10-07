from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicGameProperty
from ...enum_types import _enum_object_property_types
from bpy.props import EnumProperty


@node_type
class LogicNodeCopyProperty(LogicNodeActionType):
    bl_idname = "NLCopyPropertyFromObject"
    bl_label = "Copy From Object"
    bl_icon = 'PASTEDOWN'
    nl_category = "Objects"
    nl_subcat = 'Properties'
    nl_module = 'actions'
    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Copy From")
        self.add_input(NodeSocketLogicObject, "To")
        self.add_input(NodeSocketLogicGameProperty, "Property", {'ref_index': 1})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    nl_class = "ULCopyProperty"

    def get_input_names(self):
        return [
            "condition",
            "from_object",
            "to_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", self.mode)]

    def get_output_names(self):
        return ['OUT']
