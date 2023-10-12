from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicCondition
from bpy.props import BoolProperty


@node_type
class LogicNodeOnce(LogicNodeConditionType):
    bl_idname = "NLConditionOnceNode"
    bl_label = "Once"
    nl_module = 'uplogic.nodes.conditions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        if self.advanced:
            self.inputs[2].enabled = True
        else:
            self.inputs[2].enabled = False

    advanced: BoolProperty(
        name='Offline Reset',
        description='Show Timer for when to reset if tree is inactive. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicBoolean, "Repeat")
        self.add_input(NodeSocketLogicFloatPositive, 'Reset After', {'value': .5})
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Reset Timer')

    nl_class = "ULOnce"

    def get_input_names(self):
        return ["input_condition", 'repeat', 'reset_time']
