from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import BoolProperty


@node_type
class LogicNodeOnValueChanged(LogicNodeConditionType):
    bl_idname = "NLConditionValueChanged"
    bl_label = "On Value Changed"
    bl_description = 'Check if a value has changed'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOnValueChanged"

    initialize: BoolProperty(
        description=(
            'Ignore change from NONE to the first actual value'
        ))

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Value", 'current_value')
        self.add_output(NodeSocketLogicCondition, "If Changed", 'OUT')
        self.add_output(NodeSocketLogicParameter, "Old", 'OLD')
        self.add_output(NodeSocketLogicParameter, "New", 'NEW')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "initialize", text="Initialize")

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["current_value"]

    def get_attributes(self):
        return [("initialize", self.initialize)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT', "OLD", "NEW"]
