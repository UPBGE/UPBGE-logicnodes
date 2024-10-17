from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicGameProperty
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicDictionary
from ...enum_types import _enum_object_property_types
from bpy.props import EnumProperty


@node_type
class LogicNodeToggleProperty(LogicNodeActionType):
    bl_idname = "NLToggleGameObjectGamePropertyActionNode"
    bl_label = "Toggle Object Property"
    bl_description = 'Toggle the value of a property on an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULToggleProperty"

    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicGameProperty, "Property", 'property_name', {'ref_index': 1})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name"
        ]

    def get_attributes(self):
        return [("mode", self.mode)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
