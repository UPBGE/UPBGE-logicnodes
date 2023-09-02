from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_type_casts
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeTypecast(LogicNodeParameterType):
    bl_idname = "NLParameterTypeCast"
    bl_label = "Typecast Value"
    nl_category = "Python"
    nl_module = 'parameters'
    to_type: EnumProperty(items=_enum_type_casts, update=update_draw)

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicParameter, "Value")

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'to_type', text='')

    def get_netlogic_class_name(self):
        return "ULTypeCastValue"

    def get_input_names(self):
        return ["value"]

    def get_attributes(self):
        return [('to_type', f'"{self.to_type}"')]

    def get_output_names(self):
        return ["OUT"]
