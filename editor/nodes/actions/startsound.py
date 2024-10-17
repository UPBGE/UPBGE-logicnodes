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
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicPython
from bpy.props import EnumProperty
from bpy.props import BoolProperty


_sound_types = [
    ('0', '2D Sound', ''),
    ('1', '2D Sample', ''),
    (None),
    ('2', '3D Sound', ''),
    ('3', '3D Sample', ''),
    # (None),
    # ('4', 'Speaker', '')
]


@node_type
class LogicNodeStartSound(LogicNodeActionType):
    bl_idname = "LogicNodeStartSound"
    bl_label = "Start Sound"
    bl_description = 'Start a sound or snippet'
    bl_width_default = 200
    nl_module = 'uplogic.nodes.actions'
    nl_class = "StartSoundNode"
    
    def update_draw(self, context=None):
        names = [
            '2D Sound',
            '2D Sample',
            '3D Sound',
            '3D Sample'
        ]
        self.nl_label = names[int(self.mode)]
        self.inputs[1].enabled = int(self.mode) > 1 and self.use_speaker
        self.inputs[2].enabled = int(self.mode) > 1 and not self.use_speaker
        self.inputs[4].enabled = self.inputs[5].enabled = int(self.mode) in [1, 3]
        self.inputs[6].enabled = int(self.mode) > 1
        self.inputs[7].enabled = self.inputs[8].enabled = self.inputs[6].default_value and self.inputs[3].enabled
        self.inputs[13].enabled = int(self.mode) < 2
        state = self.advanced and int(self.mode) > 1
        for i in [15, 16, 17, 18]:
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

    update_running: BoolProperty(
        name='Update Running',
        description="Update the last started sound using this node's values",
        update=update_draw
    )

    use_speaker: BoolProperty(
        name='Use Speaker',
        description="Use an object as a transformation reference for this sound",
        update=update_draw
    )

    mode: EnumProperty(
        items=_sound_types,
        name='Sound Type',
        default='2',
        update=update_draw,
        description='Define a way to play the sound'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Start Sound", 'condition')
        self.add_input(NodeSocketLogicObject, "Speaker", 'speaker')
        self.add_input(NodeSocketLogicVectorXYZ, "Position", 'speaker')
        self.add_input(NodeSocketLogicSoundFile, "Sound File", 'sound')
        self.add_input(NodeSocketLogicFloatPositive, "Start Time", 'start_time')
        self.add_input(NodeSocketLogicFloatPositive, "End Time", 'end_time')
        self.add_input(NodeSocketLogicBoolean, "Use Occlusion", 'occlusion')
        self.add_input(NodeSocketLogicFloatFactor, 'Transition', 'transition', {'default_value': .1})
        self.add_input(NodeSocketLogicFloatFactor, 'Lowpass', 'cutoff', {'default_value': .1})
        self.add_input(NodeSocketLogicLoopCount, "Mode", 'loop_count')
        self.add_input(NodeSocketLogicFloatPositive, "Pitch", 'pitch', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", 'speed', {'default_value': 1.0, 'enabled': False})
        self.add_input(NodeSocketLogicFloatPositive, "Volume", 'volume', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatFactor, 'Lowpass', 'lowpass', {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Enable Reverb", 'reverb', {'enabled': False})
        self.add_input(NodeSocketLogicFloatPositive, "Attenuation", 'attenuation', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Reference Distance", 'distance_ref', {'default_value': 1.0})
        self.add_input(NodeSocketLogicVectorXY, "Cone Inner / Outer", 'cone_angle', {'default_value': (360., 360.)})
        self.add_input(NodeSocketLogicFloat, "Cone Outer Volume", 'cone_outer_volume', {'default_value': 0.0})
        self.add_input(NodeSocketLogicBoolean, "Ignore Timescale", 'ignore_timescale')
        self.add_output(NodeSocketLogicCondition, 'On Start', 'DONE')
        self.add_output(NodeSocketLogicCondition, 'On Finish', 'ON_FINISH')
        self.add_output(NodeSocketLogicPython, 'Sound', 'HANDLE')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        if int(self.mode) > 1:
            layout.prop(self, 'advanced', text='Show Advanced Options')
            layout.prop(self, 'use_speaker', text='Use Speaker')
        layout.prop(self, 'mode', text='')
        layout.prop(self, 'update_running', text='Update Running')
        layout.separator()

    def get_attributes(self):
        return [
            ('mode', self.mode),
            ('update_running', self.update_running)
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["DONE", 'ON_FINISH', "HANDLE"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "speaker",
            'speaker',
            "sound",
            "start_time",
            "end_time",
            'occlusion',
            'transition',
            'cutoff',
            "loop_count",
            "pitch",
            "speed",
            "volume",
            'lowpass',
            'reverb',
            "attenuation",
            "distance_ref",
            "cone_angle",
            "cone_outer_volume",
            'ignore_timescale'
        ]
