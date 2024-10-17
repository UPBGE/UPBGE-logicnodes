from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type
from ...sockets.socket import SOCKET_COLOR_CONDITION
from ...enum_types import _logic_gates_list
from bpy.props import EnumProperty



@node_type
class LogicNodeLogicGateList(LogicNodeConditionType):
    bl_idname = "LogicNodeLogicGateList"
    bl_label = "Gate List"
    bl_description = 'Logical operation using two or more conditions'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULLogicGateList"

    gate: EnumProperty(items=_logic_gates_list, name='Gate Type')

    search_tags = [
        ['Logic Gate List', {}],
        ['And List', {'nl_label': 'And'}],
        ['Or List', {'gate': '1', 'nl_label': 'Or'}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'item')
        self.add_input(NodeSocketLogicCondition, "Condition", 'item')
        self.add_output(NodeSocketLogicCondition, "Result", 'OUT')
        LogicNodeConditionType.init(self, context)

    def set_new_input_name(self):
        self.inputs[-1].name = 'Condition'

    def draw_buttons(self, context, layout) -> None:
        op = layout.operator('logic_nodes.add_socket')
        op.socket_type = 'NodeSocketLogicConditionItem'
        layout.prop(self, 'gate', text='')

    def get_output_names(self):
        return ['OUT']

    def setup(
        self,
        cell_varname,
        uids
    ):
        items = ''
        for socket in self.inputs:
            field_value = None
            if socket.linked_valid:
                field_value = self.get_linked_value(
                    socket,
                    uids
                )
            else:
                field_value = socket.get_default_value()
            items += f'{field_value}, '
        items = items[:-2]
        attributes = f'        {cell_varname}.items = [{items}]\n'
        attributes += f'        {cell_varname}.gate = {self.gate}\n'
        return attributes
