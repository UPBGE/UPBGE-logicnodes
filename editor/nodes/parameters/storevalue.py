from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from bpy.props import BoolProperty


@node_type
class LogicNodeStoreValue(LogicNodeParameterType):
    bl_idname = "NLStoreValue"
    bl_label = "Store Value"
    nl_category = "Values"
    nl_module = 'parameters'

    initialize: BoolProperty(
        name='Initialize',
        description='Store a value in the first frame to avoid NoneType issues',
        default=True
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicValue, "Value")
        self.add_output(NodeSocketLogicParameter, "Stored Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "initialize")

    def get_attributes(self):
        return [("initialize", self.initialize)]

    def get_input_names(self):
        return ['condition', 'value']

    def get_netlogic_class_name(self):
        return "ULStoreValue"

    def get_output_names(self):
        return ["OUT"]
