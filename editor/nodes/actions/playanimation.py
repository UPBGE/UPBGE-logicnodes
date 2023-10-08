from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicAnimation
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicPlayMode
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBlendMode
from ...sockets import NodeSocketLogicFloatFactor
from bpy.props import BoolProperty


@node_type
class LogicNodePlayAnimation(LogicNodeActionType):
    bl_idname = "NLActionPlayActionNode"
    bl_label = "Play Animation"
    nl_module = 'actions'
    nl_class = "ULPlayAction"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[6].enabled = False
        if self.inputs[7].value == 'bge.logic.KX_ACTION_MODE_LOOP':
            self.inputs[8].enabled = False
        else:
            self.inputs[8].enabled = True
        adv = [8, 9, 10, 11, 12]
        for x in adv:
            self.inputs[x].enabled = self.advanced

    advanced: BoolProperty(
        name='Advanced',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object / Armature")
        self.add_input(NodeSocketLogicAnimation, "Action")
        self.add_input(NodeSocketLogicFloat, "Start")
        self.add_input(NodeSocketLogicFloat, "End")
        self.add_input(NodeSocketLogicIntegerPositive, "Layer")
        self.add_input(NodeSocketLogicIntegerPositive, "Priority", {'enabled': False})
        self.add_input(NodeSocketLogicPlayMode, "Play Mode")
        self.add_input(NodeSocketLogicBoolean, "Stop When Done", {'enabled': False, 'value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Layer Weight", {'enabled': False, 'value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", {'enabled': False, 'value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Blendin", {'enabled': False})
        self.add_input(NodeSocketLogicBlendMode, "Blend Mode", {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Started")
        self.add_output(NodeSocketLogicCondition, "Running")
        self.add_output(NodeSocketLogicCondition, "On Finish")
        self.add_output(NodeSocketLogicFloat, "Current Frame")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "action_name",
            "start_frame",
            "end_frame",
            "layer",
            "priority",
            "play_mode",
            "stop",
            "layer_weight",
            "speed",
            "blendin",
            "blend_mode"
        ]

    def get_output_names(self):
        return ["STARTED", "RUNNING", "FINISHED", "FRAME"]
