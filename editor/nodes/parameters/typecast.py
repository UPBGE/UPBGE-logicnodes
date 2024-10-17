from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_type_casts
from bpy.props import EnumProperty


@node_type
class LogicNodeTypecast(LogicNodeParameterType):
    bl_idname = "NLParameterTypeCast"
    bl_label = "Typecast Value"
    bl_description = 'Convert a value to a different data type'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULTypeCastValue"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.outputs[0].enabled = self.to_type == 'int'
        self.outputs[1].enabled = self.to_type == 'bool'
        self.outputs[2].enabled = self.to_type == 'str'
        self.outputs[3].enabled = self.to_type == 'float'

    to_type: EnumProperty(items=_enum_type_casts, update=update_draw, name='To Type')

    def init(self, context):
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_output(NodeSocketLogicInteger, "Integer", 'OUT')
        self.add_output(NodeSocketLogicBoolean, "Boolean", 'OUT')
        self.add_output(NodeSocketLogicString, "String", 'OUT')
        self.add_output(NodeSocketLogicFloat, "Float", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'to_type', text='')

    def get_attributes(self):
        return [('to_type', repr(self.to_type))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["value"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['OUT', 'OUT', 'OUT', 'OUT']
