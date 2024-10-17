from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicSoundFile
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicLoopCount
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicPython
from bpy.props import BoolProperty


@node_type
class LogicNodeSound3D(LogicNodeActionType):
    bl_idname = "NLActionStart3DSoundAdv"
    bl_label = "3D Sound"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStartSound3D"
    deprecated = True

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[4].enabled = self.inputs[5].enabled = self.inputs[3].default_value
        state = self.advanced
        for i in [9, 10, 11, 12, 13, 14]:
            ipt = self.inputs[i]
            if ipt.is_linked:
                ipt.enabled = True
            else:
                ipt.enabled = state

    advanced: BoolProperty(
        name='Advanced Features',
        description='Show advanced features for this sound. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Speaker", 'speaker')
        self.add_input(NodeSocketLogicSoundFile, "Sound File")
        self.add_input(NodeSocketLogicBoolean, "Use Occlusion")
        self.add_input(NodeSocketLogicFloatFactor, 'Transition', None, {'default_value': .1})
        self.add_input(NodeSocketLogicFloatFactor, 'Lowpass', None, {'default_value': .1})
        self.add_input(NodeSocketLogicLoopCount, "Mode")
        self.add_input(NodeSocketLogicFloatPositive, "Pitch", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Volume", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Enable Reverb")
        self.add_input(NodeSocketLogicFloatPositive, "Attenuation", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Reference Distance", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicVectorXY, "Cone Inner / Outer", None, {'default_value': (360., 360.)})
        self.add_input(NodeSocketLogicFloat, "Cone Outer Volume", None, {'default_value': 0.0})
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale")
        self.add_output(NodeSocketLogicCondition, 'On Start')
        self.add_output(NodeSocketLogicCondition, 'On Finish')
        self.add_output(NodeSocketLogicPython, 'Sound')
        LogicNodeActionType.init(self, context)


    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    def get_input_names(self):
        return [
            "condition",
            "speaker",
            "sound",
            'occlusion',
            'transition',
            'cutoff',
            "loop_count",
            "pitch",
            "volume",
            'reverb',
            "attenuation",
            "distance_ref",
            "cone_angle",
            "cone_outer_volume",
            'ignore_timescale'
        ]
