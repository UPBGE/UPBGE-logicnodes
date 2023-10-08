from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicObjectName
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicBitMask
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_spawn_types
from bpy.props import BoolProperty
from bpy.props import EnumProperty


@node_type
class LogicNodeSpawnPool(LogicNodeActionType):
    bl_idname = "LogicNodeSpawnPool"
    bl_label = "Spawn Pool"
    nl_module = 'actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        simple = self.spawn_type in ['Simple', 'Instance']
        self.inputs[0].enabled = not self.create_on_init
        self.inputs[6].enabled = not simple
        self.inputs[7].enabled = not simple
        self.outputs[3].enabled = not simple
        self.outputs[4].enabled = not simple
        self.outputs[5].enabled = not simple
        self.outputs[0].enabled = not self.create_on_init
        self.outputs[2].enabled = not simple
        self.outputs[3].enabled = not simple
        self.outputs[4].enabled = not simple
        self.outputs[5].enabled = not simple
        self.outputs[6].enabled = not simple

    create_on_init: BoolProperty(
        name='Startup',
        description='Create Pool on Game Start',
        default=True,
        update=update_draw
    )

    spawn_type: EnumProperty(
        items=_enum_spawn_types,
        name="Spawn Behavior",
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Create Pool")
        self.add_input(NodeSocketLogicCondition, "Spawn")
        self.add_input(NodeSocketLogicObject, "Spawner")
        self.add_input(NodeSocketLogicObjectName, "Object Instance")
        self.add_input(NodeSocketLogicIntegerPositive, "Amount", {'value': 10})
        self.add_input(NodeSocketLogicIntegerPositive, "Life", {'value': 3})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", {'value': 75.0})
        self.add_input(NodeSocketLogicBitMask, "Bitmask")
        self.add_input(NodeSocketLogicBoolean, "Visualize")
        self.add_output(NodeSocketLogicCondition, "Pool Created")
        self.add_output(NodeSocketLogicCondition, "Spawned")
        self.add_output(NodeSocketLogicCondition, "On Hit")
        self.add_output(NodeSocketLogicObject, "Hit Object")
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Point")
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Normal")
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Direction")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'create_on_init', text='On Startup')
        layout.prop(self, 'spawn_type', text='')

    nl_class = "ULSpawnPool"

    def get_input_names(self):
        return [
            "condition",
            'spawn',
            "spawner",
            "object_instance",
            "amount",
            "life",
            "speed",
            "bitmask",
            "visualize"
        ]

    def get_attributes(self):
        return [
            ("create_on_init", self.create_on_init),
            ("spawn_type", self.spawn_type)
        ]

    def get_output_names(self):
        return [
            'OUT',
            'SPAWNED',
            'ONHIT',
            'HITOBJECT',
            'HITPOINT',
            'HITNORMAL',
            'HITDIR'
        ]
