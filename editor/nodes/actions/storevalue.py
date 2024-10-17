from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from bpy.props import BoolProperty
from ....utilities import WARNING_MESSAGES


@node_type
class LogicNodeStoreValue(LogicNodeActionType):
    bl_idname = "NLStoreValue"
    bl_label = "Store Value"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStoreValue"
    bl_description = 'Store a value for later use'

    initialize: BoolProperty(
        name='Initialize',
        description='Store a value in the first frame to avoid NoneType issues',
        default=True
    )

    def check(self, tree):
        super().check(tree)
        if len(self.outputs) != 2:
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(f"Node '{self.name}' in tree '{tree.name}' changed outputs. Re-Add to avoid issues.")
            self.use_custom_color = True
            self.color = (.8, .6, 0)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        self.add_output(NodeSocketLogicParameter, "Stored Value", 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "initialize")

    def get_attributes(self):
        return [("initialize", self.initialize)]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ['condition', 'value']

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['DONE', "OUT"]
