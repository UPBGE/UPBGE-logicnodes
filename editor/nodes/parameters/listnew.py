from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicListItem


@node_type
class LogicNodeListNew(LogicNodeParameterType):
    bl_idname = "NLInitNewList"
    bl_label = "List From Items"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicListItem, 'Item')
        self.add_input(NodeSocketLogicListItem, 'Item')
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        op = layout.operator('logic_nodes.add_socket')
        op.socket_type = 'NLListItemSocket'

    def set_new_input_name(self):
        self.inputs[-1].name = 'Item'

    def setup(
        self,
        cell_varname,
        uids
    ):
        items = ''
        for socket in self.inputs:
            field_value = None
            if socket.linked_valid:
                field_value = self.get_linked_socket_field_value(
                    socket,
                    cell_varname,
                    None,
                    uids
                )
            else:
                field_value = socket.get_unlinked_value()
            items += f'{field_value}, '
        items = items[:-2]
        return f'        {cell_varname}.items = [{items}]\n'

    def get_output_names(self):
        return ['LIST']

    nl_class = "ULListFromItems"
