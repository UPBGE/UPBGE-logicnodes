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
    nl_category = "Physics"
    nl_subcat = 'Vehicle'
    nl_module = 'actions'
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
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Vehicle")
        self.add_input(NodeSocketLogicIntegerPositive, "Wheels", {'value': 2})
        self.add_input(NodeSocketLogicFloat, "Steer")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    def get_input_names(self):
        return ["condition", "vehicle", "wheelcount", 'power']

    def get_attributes(self):
        return [
            ("value_type", f'"{self.value_type}"'),
        ]
