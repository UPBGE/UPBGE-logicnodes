from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_vehicle_axis
from bpy.props import EnumProperty


@node_type
class LogicNodeVehicleSteer(LogicNodeActionType):
    bl_idname = "NLVehicleApplySteering"
    bl_label = "Steer"
    bl_description = 'Steer the front wheels of a vehicle'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULVehicleApplySteering"

    search_tags = [
        ['Steer Vehicle', {}]
    ]

    def update_draw(self, context=None):
        self.inputs[2].enabled = self.value_type != 'ALL'

    value_type: EnumProperty(
        name='Axis',
        items=_enum_vehicle_axis,
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Vehicle", 'vehicle')
        self.add_input(NodeSocketLogicIntegerPositive, "Wheels", 'wheelcount', {'default_value': 2})
        self.add_input(NodeSocketLogicFloat, "Steer", 'power')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["condition", "vehicle", "wheelcount", 'power']

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [
            ("value_type", repr(self.value_type)),
        ]
