from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicIntegerPositive
from ...enum_types import _enum_vehicle_axis
from bpy.props import EnumProperty


@node_type
class LogicNodeVehicleAccelerate(LogicNodeActionType):
    bl_idname = "NLVehicleApplyEngineForce"
    bl_label = "Accelerate"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULVehicleApplyForce"

    search_tags = [
        ['Accelerate Vehicle', {}]
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
        self.add_input(NodeSocketLogicFloatPositive, "Power", {'value': 1})
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
