from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicDictionary
from ...enum_types import _serialize_types
from bpy.props import EnumProperty
import bpy


@node_type
class LogicNodeRebuildData(LogicNodeParameterType):
    bl_idname = "LogicNodeRebuildData"
    bl_label = "Rebuild Data"
    bl_description = 'Parse string data from a "Serialize" node'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULRebuildData"

    def update_draw(self, context=None):
        self.inputs[0].enabled = self.read_as == 'GameObj'

    read_as: EnumProperty(
        items=_serialize_types,
        name='Read As',
        description='Select the correct format to read a python object',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicDictionary, "Data", 'data')
        self.add_output(NodeSocketLogicParameter, 'Data', 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'read_as', text='')

    def get_attributes(self):
        return [("read_as", repr(self.read_as))]

    def get_input_names(self):  # XXX Remove for 5.0
        if len(self.inputs) < 2:
            self.rebuild()
        return ['condition', "data"]

    def get_output_names(self):  # XXX Remove for 5.0
        return ['OUT']
