from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _serialize_types
from bpy.props import EnumProperty


@node_type
class LogicNodeSerializeData(LogicNodeParameterType):
    bl_idname = "LogicNodeSerializeData"
    bl_label = "Serialize Data"
    bl_icon = 'ALIGN_FLUSH'
    nl_category = "Network"
    nl_module = 'parameters'

    serialize_as: EnumProperty(
        items=_serialize_types,
        name='Serialize As',
        description='Select the correct format to serialize a python object'
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicParameter, "Data")
        self.add_output(NodeSocketLogicParameter, 'Data')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'serialize_as', text='')

    def get_netlogic_class_name(self):
        return "ULSerializeData"

    def get_attributes(self):
        return [("serialize_as", f'"{self.serialize_as}"')]

    def get_input_names(self):
        return ["data"]

    def get_output_names(self):
        return ['OUT']
