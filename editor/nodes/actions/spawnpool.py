from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
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
    bl_description = 'Add a spawn pool to avoid dynamically creating objects'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSpawnPool"

    def update_draw(self, context=None):
        if not self.ready:
            return
        simple = self.spawn_type in ['0', '3']
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
        self.add_input(NodeSocketLogicCondition, "Create Pool", 'condition')
        self.add_input(NodeSocketLogicCondition, "Spawn", 'spawn')
        self.add_input(NodeSocketLogicObject, "Spawner", 'spawner')
        self.add_input(NodeSocketLogicObject, "Object Instance", 'object_instance', {'allow_owner': False})
        self.add_input(NodeSocketLogicIntegerPositive, "Amount", 'amount', {'default_value': 10})
        self.add_input(NodeSocketLogicIntegerPositive, "Life", 'life', {'default_value': 3})
        self.add_input(NodeSocketLogicFloatPositive, "Speed", 'speed', {'default_value': 75.0})
        self.add_input(NodeSocketLogicBitMask, "Bitmask", 'bitmask')
        self.add_input(NodeSocketLogicBoolean, "Visualize", 'visualize')
        self.add_output(NodeSocketLogicCondition, "Pool Created", 'OUT')
        self.add_output(NodeSocketLogicCondition, "Spawned", 'SPAWNED')
        self.add_output(NodeSocketLogicCondition, "On Hit", 'ONHIT')
        self.add_output(NodeSocketLogicObject, "Hit Object", 'HITOBJECT')
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Point", 'HITPOINT')
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Normal", 'HITNORMAL')
        self.add_output(NodeSocketLogicVectorXYZ, "Hit Direction", 'HITDIR')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'create_on_init', text='On Startup')
        layout.prop(self, 'spawn_type', text='')

    # XXX: Remove for 5.0
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

    # XXX: Remove for 5.0
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
