from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_vehicle_axis
from bpy.props import EnumProperty


@node_type
class LoigcNodeVehicleSetAttributes(LogicNodeActionType):
    bl_idname = "NLVehicleSetAttributes"
    bl_label = "Set Vehicle Attributes"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULVehicleSetAttributes"
    bl_width_default = 180
    bl_description = 'Set an attribute of a vehicle'

    search_tags = [
        ['Set Vehicle Attributes', {}]
    ]

    def update_draw(self, context=None):
        self.inputs[2].enabled = self.value_type != 'ALL'
        ipts = self.inputs
        ipts[4].enabled = ipts[3].default_value
        ipts[6].enabled = ipts[5].default_value
        ipts[8].enabled = ipts[7].default_value
        ipts[10].enabled = ipts[9].default_value

    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Collider", 'vehicle')
        self.add_input(NodeSocketLogicIntegerPositive, "Wheels", 'wheelcount', {'default_value': 2})
        self.add_input(NodeSocketLogicBoolean, "Suspension", 'set_suspension_compression')
        self.add_input(NodeSocketLogicFloat, "", 'suspension_compression')
        self.add_input(NodeSocketLogicBoolean, "Stiffness", 'set_suspension_stiffness')
        self.add_input(NodeSocketLogicFloat, "", 'suspension_stiffness')
        self.add_input(NodeSocketLogicBoolean, "Damping", 'set_suspension_damping')
        self.add_input(NodeSocketLogicFloat, "", 'suspension_damping')
        self.add_input(NodeSocketLogicBoolean, "Friction", 'set_tyre_friction')
        self.add_input(NodeSocketLogicFloat, "", 'tyre_friction')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    # XXX Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "vehicle",
            "wheelcount",
            'set_suspension_compression',
            'suspension_compression',
            'set_suspension_stiffness',
            'suspension_stiffness',
            'set_suspension_damping',
            'suspension_damping',
            'set_tyre_friction',
            'tyre_friction'
        ]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [
            ("value_type", repr(self.value_type)),
        ]
