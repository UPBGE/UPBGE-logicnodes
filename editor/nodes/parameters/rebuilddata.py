from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _serialize_types
from bpy.props import EnumProperty


@node_type
class LogicNodeRebuildData(LogicNodeParameterType):
    bl_idname = "LogicNodeRebuildData"
    bl_label = "Rebuild Data"
    bl_icon = 'OBJECT_HIDDEN'
    nl_module = 'parameters'

    read_as: EnumProperty(
        items=_serialize_types,
        name='Read As',
        description='Select the correct format to read a python object'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Data")
        self.add_output(NodeSocketLogicParameter, 'Data')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'read_as', text='')

    nl_class = "ULRebuildData"

    def get_attributes(self):
        return [("read_as", f'"{self.read_as}"')]

    def get_input_names(self):
        return ["data"]

    def get_output_names(self):
        return ['OUT']
