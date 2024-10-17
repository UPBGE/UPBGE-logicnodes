from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicIntegerPositive
from ...enum_types import _enum_vehicle_axis
from bpy.props import EnumProperty


@node_type
class LogicNodeVehicleBrake(LogicNodeActionType):
    bl_idname = "NLVehicleApplyBraking"
    bl_label = "Brake"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULVehicleApplyBraking"
    bl_description = 'Apply a braking force to a vehicle according to its setup'

    search_tags = [
        ['Brake Vehicle', {}]
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
        self.add_input(NodeSocketLogicFloatPositive, "Power", 'power', {'default_value': 1})
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