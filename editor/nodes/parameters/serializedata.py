from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicDictionary
from ...enum_types import _serialize_types
from bpy.props import EnumProperty


@node_type
class LogicNodeSerializeData(LogicNodeParameterType):
    bl_idname = "LogicNodeSerializeData"
    bl_label = "Serialize Data"
    bl_description = 'Serialize a set of data'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULSerializeData"

    serialize_as: EnumProperty(
        items=_serialize_types,
        name='Serialize As',
        description='Select the correct format to serialize a python object'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, "Data", 'data')
        self.add_output(NodeSocketLogicDictionary, 'Data', 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'serialize_as', text='')

    def get_attributes(self):
        return [("serialize_as", repr(self.serialize_as))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["data"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['OUT']
