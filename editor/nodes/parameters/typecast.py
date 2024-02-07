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
    nl_module = 'uplogic.nodes.parameters'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.outputs[0].enabled = self.to_type == 'int'
        self.outputs[1].enabled = self.to_type == 'bool'
        self.outputs[2].enabled = self.to_type == 'str'
        self.outputs[3].enabled = self.to_type == 'float'

    to_type: EnumProperty(items=_enum_type_casts, update=update_draw, name='To Type')

    def init(self, context):
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicInteger, "Integer")
        self.add_output(NodeSocketLogicBoolean, "Boolean")
        self.add_output(NodeSocketLogicString, "String")
        self.add_output(NodeSocketLogicFloat, "Float")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'to_type', text='')

    nl_class = "ULTypeCastValue"

    def get_input_names(self):
        return ["value"]

    def get_attributes(self):
        return [('to_type', f'"{self.to_type}"')]

    def get_output_names(self):
        return ['OUT', 'OUT', 'OUT', 'OUT']
