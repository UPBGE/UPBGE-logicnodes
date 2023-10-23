from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...enum_types import _enum_msg_types
from bpy.props import EnumProperty


@node_type
class LogicNodePrint(LogicNodeActionType):
    bl_idname = "NLActionPrint"
    bl_label = "Print"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPrintValue"

    msg_type: EnumProperty(
        items=_enum_msg_types,
        name='Type',
        description=(
            'The Message Type defines the color when'
            'using the on-screen console'
        )
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", {'default_value': True, 'show_prop': True})
        self.add_input(NodeSocketLogicString, "Value")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'msg_type', text='')

    def get_attributes(self):
        return [("msg_type", f'"{self.msg_type}"')]

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "value"]
